"""
Generates XML entries for Isaac mods using LLM + schema context.

Falls back to programmatic generation when no LLM is available or LLM
output fails validation.
"""

import re
from typing import Any, Dict, List, Optional

from loguru import logger

from isaac_agent.core.state import (
    GeneratedXml,
    XmlEntry,
    XmlFileSchema,
)


class XmlGenerationContext:
    """Tracks incrementing IDs and name derivation during XML generation."""

    def __init__(self, mod_name: str = "isaac_mod", task_title: str = ""):
        self._counters: Dict[str, int] = {}
        self.mod_name = mod_name
        self._task_title = task_title or mod_name

    def next_id(self, key: str = "default", base: int = 1000) -> int:
        if key not in self._counters:
            self._counters[key] = base
        val = self._counters[key]
        self._counters[key] += 1
        return val

    def derived_name(self, task_title: str = "") -> str:
        safe = "".join(c if c.isalnum() else "_" for c in task_title)
        safe = safe.strip("_")[:30]
        if not safe:
            safe = self.mod_name
        return safe

    def safe_name(self) -> str:
        name = self._task_title or self.mod_name
        safe = "".join(c if c.isalnum() else "_" for c in name)
        return safe.strip("_").lower()[:40] or "isaac_mod"


# Programmatic defaults per XML file type
SMART_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "items.xml": {
        "id": lambda ctx: ctx.next_id("item", 1000),
        "name": lambda ctx: ctx.derived_name(),
        "description": lambda ctx: "A custom item",
        "type": "active",
        "quality": "2",
        "cache": "",
        "tags": "",
        "gfx": lambda ctx: f"gfx/ui/items/{ctx.safe_name()}.png",
        "maxcharges": "6",
        "chargetype": "normal",
        "hidden": "false",
        "special": "false",
    },
    # Per-type overrides for items.xml — selected based on scaffold_type
    "items.xml_passive": {
        "id": lambda ctx: ctx.next_id("item", 1000),
        "name": lambda ctx: ctx.derived_name(),
        "description": lambda ctx: "A passive item",
        "quality": "2",
        "cache": "damage",
        "tags": "",
        "gfx": lambda ctx: f"gfx/ui/items/{ctx.safe_name()}.png",
        "hidden": "false",
        "special": "false",
    },
    "items.xml_active": {
        "id": lambda ctx: ctx.next_id("item", 1000),
        "name": lambda ctx: ctx.derived_name(),
        "description": lambda ctx: "An active item",
        "quality": "2",
        "tags": "",
        "gfx": lambda ctx: f"gfx/ui/items/{ctx.safe_name()}.png",
        "maxcharges": "6",
        "chargetype": "normal",
        "hidden": "false",
        "special": "false",
    },
    "items.xml_familiar": {
        "id": lambda ctx: ctx.next_id("item", 1000),
        "name": lambda ctx: ctx.derived_name(),
        "description": lambda ctx: "A familiar item",
        "quality": "2",
        "cache": "damage",
        "tags": "",
        "gfx": lambda ctx: f"gfx/ui/items/{ctx.safe_name()}.png",
        "hidden": "false",
        "special": "false",
    },
    "entities2.xml": {
        "id": lambda ctx: ctx.next_id("entity", 100),
        "name": lambda ctx: ctx.derived_name(),
        "variant": lambda ctx: ctx.next_id("variant", 100),
        "baseHP": "20",
        "boss": "0",
        "champion": "1",
        "collisionDamage": "1",
        "collisionMass": "3",
        "collisionRadius": "12",
        "friction": "1",
        "shadowSize": "16",
        "stageHP": "0",
        "tags": "",
        "numGridCollisionPoints": "24",
        "anm2path": lambda ctx: f"gfx/{ctx.safe_name()}.anm2",
    },
    "players.xml": {
        "name": lambda ctx: ctx.derived_name(),
        "skin": lambda ctx: f"character_{ctx.safe_name()}.png",
        "hp": "6",
        "armor": "0",
        "black": "0",
        "bombs": "1",
        "keys": "0",
        "coins": "0",
        "canShoot": "true",
        "skinColor": "-1",
    },
    "costumes2.xml": {
        "id": lambda ctx: ctx.next_id("costume", 100),
        "anm2path": lambda ctx: f"gfx/characters/costumes/{ctx.safe_name()}.anm2",
        "type": "passive",
        "priority": "5",
        "overwriteColor": "false",
        "isFlying": "false",
        "skinColor": "0",
        "hasSkinAlt": "false",
        "hasOverlay": "false",
    },
    "pocketitems.xml": {
        "card": {
            "name": lambda ctx: ctx.derived_name(),
            "description": lambda ctx: "A custom card",
            "hud": lambda ctx: ctx.derived_name(),
            "type": "special",
            "mimiccharge": "2",
        },
        "pilleffect": {
            "name": lambda ctx: ctx.derived_name(),
            "class": "2",
            "mimiccharge": "1",
        },
    },
    "itempools.xml": {
        "Name": lambda ctx: ctx.derived_name(),
        "Weight": "1",
        "DecreaseBy": "1",
        "RemoveOn": "0.1",
    },
}


class XmlGenerator:
    """Generates XML entries using LLM + schema context, with programmatic fallback."""

    def __init__(self, schemas: List[XmlFileSchema], llm=None):
        self._schema_by_filename: Dict[str, XmlFileSchema] = {}
        for s in schemas:
            self._schema_by_filename[s.filename] = s
        self.llm = llm
        self._shared_context: Optional[XmlGenerationContext] = None

    def get_schema(self, filename: str) -> Optional[XmlFileSchema]:
        return self._schema_by_filename.get(filename)

    def generate(
        self,
        xml_file: str,
        task_title: str,
        task_description: str,
        lua_code: str,
        scaffold_type: str,
        dlc_version: str = "REP+",
    ) -> GeneratedXml:
        """
        Generate XML entries for a single XML file.

        Tries LLM first if available; falls back to programmatic.
        """
        schema = self._schema_by_filename.get(xml_file)
        if not schema:
            logger.warning(f"No schema for {xml_file}, skipping")
            return GeneratedXml(
                scaffold_type=scaffold_type,
                xml_file=xml_file,
                folder="content",
                entries=[],
                generated_by="none",
            )

        # Use shared context if available, otherwise create a new one
        ctx = self._shared_context or XmlGenerationContext(
            mod_name="".join(c if c.isalnum() else "_" for c in task_title).strip("_").lower()
        )

        if self.llm:
            try:
                result = self._llm_generate(
                    schema=schema,
                    task_title=task_title,
                    task_description=task_description,
                    lua_code=lua_code,
                    scaffold_type=scaffold_type,
                    dlc_version=dlc_version,
                )
                if result and result.entries:
                    return result
            except Exception as e:
                logger.warning(f"LLM XML generation failed for {xml_file}: {e}")

        logger.info(f"Using programmatic XML generation for {xml_file}")
        return self._programmatic_generate(
            schema=schema,
            task_title=task_title,
            task_description=task_description,
            ctx=ctx,
            scaffold_type=scaffold_type,
        )

    # ------------------------------------------------------------------
    # LLM-based generation
    # ------------------------------------------------------------------

    def _llm_generate(
        self,
        schema: XmlFileSchema,
        task_title: str,
        task_description: str,
        lua_code: str,
        scaffold_type: str,
        dlc_version: str,
    ) -> Optional[GeneratedXml]:
        """Generate XML using LLM with schema context."""
        if not self.llm:
            return None

        prompt = self._build_xml_prompt(
            schema=schema,
            task_title=task_title,
            task_description=task_description,
            lua_code=lua_code,
            scaffold_type=scaffold_type,
            dlc_version=dlc_version,
        )

        try:
            import asyncio
            from langchain_core.messages import SystemMessage, HumanMessage

            messages = [
                SystemMessage(content=prompt),
                HumanMessage(content=f"Generate the {schema.filename} entry for: {task_title}"),
            ]

            # Detect if we're in an async context
            try:
                loop = asyncio.get_running_loop()
                # We're async — need to run sync LLM in a thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    response = pool.submit(self.llm.invoke, messages).result(timeout=60)
            except RuntimeError:
                response = self.llm.invoke(messages)

            raw = response.content if hasattr(response, 'content') else str(response)
            entries = self._extract_xml_entries(raw, schema, scaffold_type)

            if entries:
                return GeneratedXml(
                    scaffold_type=scaffold_type,
                    xml_file=schema.filename,
                    folder=schema.folder if schema.folder != "unknown" else "content",
                    entries=entries,
                    generated_by="llm",
                )
        except Exception as e:
            logger.warning(f"LLM XML call failed: {e}")

        return None

    def _build_xml_prompt(
        self,
        schema: XmlFileSchema,
        task_title: str,
        task_description: str,
        lua_code: str,
        scaffold_type: str,
        dlc_version: str,
    ) -> str:
        """Build the LLM prompt for XML generation."""

        # Truncate Lua code to avoid context overflow
        lua_excerpt = lua_code[:1500]
        if len(lua_code) > 1500:
            lua_excerpt += "\n... (truncated)"

        # Build attribute list
        attr_lines = []
        for a in schema.attributes:
            req = " [REQUIRED]" if a.required else ""
            pv = f" Allowed: {a.possible_values}" if a.possible_values else ""
            attr_lines.append(f"  - {a.name} ({a.type}){req}: {a.description}{pv}")

        # Build sub-element sections
        sub_lines = []
        for se in schema.sub_elements:
            sub_lines.append(f"\n  <{se.name}> child element attributes:")
            for a in se.attributes:
                sub_lines.append(f"    - {a.name} ({a.type}): {a.description}")

        # Reference examples
        example_text = ""
        if schema.xml_examples:
            example_text = "\n--- REFERENCE EXAMPLES ---\n"
            for ex in schema.xml_examples[:2]:
                example_text += f"\n```xml\n{ex}\n```\n"

        # Tags
        tag_text = ""
        if schema.tags:
            tag_text = "\n--- KNOWN TAGS ---\n"
            for t in schema.tags[:15]:
                tag_text += f"  - {t['name']}: {t['description']}\n"

        # Determine the correct child element tag for items.xml
        child_tag = _child_tag_for_schema(schema, scaffold_type)

        tag_instruction = ""
        if schema.filename == "items.xml":
            item_type = _item_type_from_scaffold(scaffold_type)
            if item_type == "passive":
                tag_instruction = (
                    f"\nCRITICAL: Use <passive> as the element tag (NOT <item>). "
                    "Passive items REQUIRE the cache attribute (e.g., cache=\"damage\"). "
                    "Do NOT include maxcharges or chargetype."
                )
            elif item_type == "active":
                tag_instruction = (
                    f"\nCRITICAL: Use <active> as the element tag (NOT <item>). "
                    "Active items REQUIRE maxcharges and chargetype attributes. "
                    "Do NOT include cache."
                )
            elif item_type == "familiar":
                tag_instruction = (
                    f"\nCRITICAL: Use <familiar> as the element tag (NOT <item>). "
                    "Familiar items should include the cache attribute (e.g., cache=\"damage\")."
                )

        return f"""You are an expert in The Binding of Isaac: Repentance XML modding.
Generate XML entries for the file `{schema.filename}`.

Target DLC: {dlc_version}
Scaffold type: {scaffold_type}
Child element tag: <{child_tag}>{tag_instruction}

Task: {task_title}
Description: {task_description}

The Lua code uses these names/IDs (your XML must match):
```lua
{lua_excerpt}
```

--- SCHEMA for {schema.filename} ---
Root element: <{schema.root_element}>
Folder: {schema.folder} (this file adds new entries)

Attributes:
{chr(10).join(attr_lines)}
{"".join(sub_lines)}
{tag_text}
{example_text}
--- INSTRUCTIONS ---
1. Generate XML entries for the {schema.filename} file.
2. Use as many relevant attributes as possible — do NOT use just the minimum.
3. Ensure IDs and names match what the Lua code expects.
4. If the Lua code calls Isaac.GetCardIdByName("X"), use hud="X".
5. Wrap attributes in double quotes: attribute="value".
6. Return ONLY the XML, no markdown code fences, no explanations.
7. Use sensible defaults for attributes not explicitly specified in the task.
8. CRITICAL: Use <{child_tag}> as the child element tag — NOT <item>."""

    @staticmethod
    def _extract_xml_entries(raw: str, schema: XmlFileSchema, scaffold_type: str = "") -> List[XmlEntry]:
        """Parse LLM response into XmlEntry objects."""
        # Strip markdown fences if present
        raw = raw.strip()
        raw = re.sub(r'^```(?:xml)?\s*\n', '', raw)
        raw = re.sub(r'\n```\s*$', '', raw)

        entries = []

        # Determine the expected child element tag
        child_tag = _child_tag_for_schema(schema, scaffold_type)

        # Find all element tags in the XML
        tag_pattern = re.compile(rf'<{child_tag}\s+([^>]+?)(?:>(.*?)</{child_tag}>|/>)', re.DOTALL)
        for m in tag_pattern.finditer(raw):
            attr_str = m.group(1)
            attrs = {}
            for am in re.finditer(r'(\w+)="([^"]*)"', attr_str):
                attrs[am.group(1)] = am.group(2)

            sub_entries = []
            inner = m.group(2)
            if inner:
                for se in schema.sub_elements:
                    sub_pattern = re.compile(
                        rf'<{se.name}\s+([^>]+?)(?:>(.*?)</{se.name}>|/>)', re.DOTALL,
                    )
                    for sm in sub_pattern.finditer(inner):
                        sattrs = {}
                        for sam in re.finditer(r'(\w+)="([^"]*)"', sm.group(1)):
                            sattrs[sam.group(1)] = sam.group(2)
                        sub_entries.append(XmlEntry(
                            element_tag=se.name,
                            attributes=sattrs,
                        ))

            entries.append(XmlEntry(
                element_tag=child_tag,
                attributes=attrs,
                sub_elements=sub_entries,
            ))

        return entries

    # ------------------------------------------------------------------
    # Programmatic fallback
    # ------------------------------------------------------------------

    def _programmatic_generate(
        self,
        schema: XmlFileSchema,
        task_title: str,
        task_description: str,
        ctx: XmlGenerationContext,
        scaffold_type: str,
    ) -> GeneratedXml:
        """Generate XML entries programmatically using smart defaults."""
        ctx._task_title = task_title
        ctx._task_description = task_description

        defaults = SMART_DEFAULTS.get(schema.filename, {})
        child_tag = _child_tag_for_schema(schema, scaffold_type)

        # For items.xml, select per-type defaults based on scaffold_type
        if schema.filename == "items.xml":
            item_type = _item_type_from_scaffold(scaffold_type)
            typed_key = f"items.xml_{item_type}"
            if typed_key in SMART_DEFAULTS:
                defaults = SMART_DEFAULTS[typed_key]

        if not defaults:
            # Generic fallback: use schema attributes to build minimal entry
            entry_attrs = {}
            for a in schema.attributes:
                if a.required:
                    if a.name == "id" or a.type == "int":
                        entry_attrs[a.name] = str(ctx.next_id())
                    else:
                        entry_attrs[a.name] = ctx.derived_name(task_title)
            entries = [XmlEntry(element_tag=child_tag, attributes=entry_attrs)]
            return GeneratedXml(
                scaffold_type=scaffold_type,
                xml_file=schema.filename,
                folder=schema.folder if schema.folder != "unknown" else "content",
                entries=entries,
                generated_by="programmatic",
            )

        # For pocketitems.xml, defaults is keyed by sub-element type
        if schema.filename == "pocketitems.xml":
            return self._programmatic_pocketitems(schema, ctx, scaffold_type)

        # Build attributes from defaults
        attrs = {}
        for key, val in defaults.items():
            if callable(val):
                attrs[key] = str(val(ctx))
            else:
                attrs[key] = str(val)

        return GeneratedXml(
            scaffold_type=scaffold_type,
            xml_file=schema.filename,
            folder=schema.folder if schema.folder != "unknown" else "content",
            entries=[XmlEntry(element_tag=child_tag, attributes=attrs)],
            generated_by="programmatic",
        )

    def _programmatic_pocketitems(
        self,
        schema: XmlFileSchema,
        ctx: XmlGenerationContext,
        scaffold_type: str,
    ) -> GeneratedXml:
        """Special handling for pocketitems.xml (card vs pilleffect)."""
        desc = ctx._task_description.lower()
        if "pill" in desc:
            defaults = SMART_DEFAULTS["pocketitems.xml"]["pilleffect"]
            child_tag = "pilleffect"
        else:
            defaults = SMART_DEFAULTS["pocketitems.xml"]["card"]
            child_tag = "card"

        attrs = {}
        for key, val in defaults.items():
            if callable(val):
                attrs[key] = str(val(ctx))
            else:
                attrs[key] = str(val)

        return GeneratedXml(
            scaffold_type=scaffold_type,
            xml_file=schema.filename,
            folder="content",
            entries=[XmlEntry(element_tag=child_tag, attributes=attrs)],
            generated_by="programmatic",
        )

    # ------------------------------------------------------------------
    # Merging
    # ------------------------------------------------------------------

    @staticmethod
    def merge_xml_files(generated: List[GeneratedXml]) -> List[GeneratedXml]:
        """Merge GeneratedXml objects that target the same XML file."""
        by_file: Dict[str, GeneratedXml] = {}
        for g in generated:
            key = g.xml_file
            if key in by_file:
                by_file[key].entries.extend(g.entries)
                # Keep the first folder/generated_by for metadata
            else:
                by_file[key] = GeneratedXml(
                    scaffold_type=g.scaffold_type,
                    xml_file=g.xml_file,
                    folder=g.folder,
                    entries=list(g.entries),
                    generated_by=g.generated_by,
                )
        return list(by_file.values())


def _item_type_from_scaffold(scaffold_type: str) -> str:
    """Infer item type (passive/active/familiar) from scaffold_type."""
    if "passive" in scaffold_type:
        return "passive"
    if "active" in scaffold_type:
        return "active"
    if "familiar" in scaffold_type:
        return "familiar"
    return "passive"  # default


def _child_tag_for_schema(schema: XmlFileSchema, scaffold_type: str = "") -> str:
    """Determine the child element tag for a given XML file schema."""
    filename_to_tag = {
        "items.xml": _item_type_from_scaffold(scaffold_type) if scaffold_type else "passive",
        "entities2.xml": "entity",
        "players.xml": "player",
        "costumes2.xml": "costume",
        "pocketitems.xml": "card",  # default, could be "rune" or "pilleffect"
        "itempools.xml": "Pool",
        "sounds.xml": "sound",
        "stages.xml": "stage",
        "challenges.xml": "challenge",
        "babies.xml": "baby",
        "backdrops.xml": "backdrop",
        "bombcostumes.xml": "bomb",
        "bosscolors.xml": "boss",
        "bossoverlays.xml": "bossoverlay",
        "bosspools.xml": "bosspool",
        "bossportraits.xml": "bossportrait",
        "curses.xml": "curse",
        "cutscenes.xml": "cutscene",
        "fortunes.xml": "fortune",
        "giantbook.xml": "giantbook",
        "items_metadata.xml": "item_metadata",
        "locusts.xml": "locust",
        "minibosses.xml": "miniboss",
        "nightmares.xml": "nightmare",
        "playerforms.xml": "playerform",
        "preload.xml": "preload",
        "recipes.xml": "recipe",
        "rules.xml": "rule",
        "seedmenu.xml": "seedmenu",
        "seeds.xml": "seed",
        "translations.xml": "translation",
        "wisps.xml": "wisp",
        "ambush.xml": "ambush",
        "achievements.xml": "achievement",
        "music.xml": "music",
        "fxlayers.xml": "fx",
    }
    return filename_to_tag.get(schema.filename, schema.root_element)
