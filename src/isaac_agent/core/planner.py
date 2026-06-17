"""
Mod architecture planner for the Isaac AI Agent.

The planner is the NEW second stage in the workflow pipeline.
It takes a parsed TaskDefinition and designs the complete multi-file
project structure BEFORE any code is generated.

This replaces the old approach of filling a single template with all logic.
"""

import json
import re
from typing import List, Optional

from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import SystemMessage, HumanMessage
from loguru import logger

from isaac_agent.core.state import FilePlan, ModComponent, TaskDefinition
from isaac_agent.templates.reference_template import ReferenceTemplate
from isaac_agent.templates.patterns import ModArchitectureGuide, FilePattern


def _extract_json(text: str) -> dict:
    """Extract JSON object from LLM response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not extract JSON from planner response: {text[:200]}")


class ModPlanner:
    """Designs the file architecture for a mod before code generation.

    Architecture-first approach:
    1. Classify the user's request into mod component types
    2. Design the complete file tree based on component types
    3. Assign roles, required APIs, and patterns to each file
    4. Generate shared context (Mod_Data structure) for cross-file consistency
    """

    def __init__(
        self,
        reference_template: Optional[ReferenceTemplate] = None,
        architecture_guide: Optional[ModArchitectureGuide] = None,
        llm: Optional[BaseLanguageModel] = None,
    ):
        self.reference_template = reference_template or ReferenceTemplate()
        self.architecture_guide = architecture_guide or ModArchitectureGuide()
        self.llm = llm

    def classify_mod_type(self, task: TaskDefinition) -> List[ModComponent]:
        """Classify the request into one or more mod component types.

        Uses keyword analysis. When LLM is available, also uses LLM-driven
        classification for ambiguous cases.
        """
        components = []
        user_lower = task.description.lower() + " " + task.title.lower()

        # Keyword-based classification
        item_keywords = {
            "passive_item": ["被动", "passive", "被动道具", "属性", "stat", "cache", "evaluate cache"],
            "active_item": ["主动", "active", "主动道具", "使用", "use item", "charge", "充能"],
            "familiar": ["跟班", "familiar", "宠物", "召唤", "companion", "follow"],
            "room_modifier": ["房间", "room", "层", "floor", "stage"],
            "player_modifier": ["玩家", "player", "角色", "character", "初始"],
            "custom_entity": ["敌人", "enemy", "实体", "entity", "boss"],
        }

        for comp_type, keywords in item_keywords.items():
            if any(kw in user_lower for kw in keywords):
                components.append(ModComponent(
                    component_type=comp_type,
                    name=task.title,
                    description=task.description,
                ))

        # Default to passive item if nothing matched
        if not components:
            components.append(ModComponent(
                component_type="passive_item",
                name=task.title,
                description=task.description,
            ))

        logger.info(f"Classified mod into components: {[c.component_type for c in components]}")
        return components

    async def _llm_plan(self, task: TaskDefinition, components: List[ModComponent]) -> List[FilePlan]:
        """Use LLM to design the file architecture."""
        patterns = self.architecture_guide.get_patterns_for_components(
            [c.component_type for c in components]
        )

        # Build the planning prompt
        pattern_lines = []
        for p in patterns:
            pattern_lines.append(
                f"  - {p.pattern_id}: {p.relative_path_template} — {p.role_description}"
            )

        system_prompt = f"""You are an expert Isaac mod architect. Design the complete file tree for a mod.

{self.reference_template.as_prompt_context()}

The user wants to create a mod with these components:
{chr(10).join(f'- {c.component_type}: {c.name} — {c.description}' for c in components)}

Available architectural patterns:
{chr(10).join(pattern_lines)}

Design the COMPLETE file tree. Output ONLY a JSON object:

{{
    "shared_context": "Mod_Data structure with all item/entity IDs and names for cross-file references",
    "files": [
        {{
            "relative_path": "scripts/items/item_name.lua",
            "role_description": "What this specific file does",
            "required_apis": ["API1", "API2"],
            "dependencies": ["other_file.lua"],
            "template_hint": "passive_item_script",
            "is_xml": false
        }}
    ]
}}

Rules:
1. ALWAYS include base files: main.lua, scripts/common.lua, scripts/data/data.lua, metadata.xml
2. When items are involved, include scripts/items/!items.lua and content/items.xml
3. Each item gets its own file under scripts/items/
4. Name item files descriptively based on the item's function
5. List only the APIs each specific file actually needs (3-5 max per file)
6. The shared_context should define the Mod_Data structure with all item IDs
7. The include chain MUST follow: main.lua -> common.lua -> data.lua + !items.lua -> individual items

CRITICAL NAMING RULES:
- ALL file names, paths, function names, and variable names MUST be in English (ASCII only, NO Chinese/Unicode characters)
- If the user's request is in Chinese, TRANSLATE the meaning to descriptive English — do NOT use pinyin or transliteration
- NEVER use placeholder names like item1, item2, Item1, Item2 — these are FORMAT examples only
- Use descriptive names based on what the item DOES: e.g., damage_booster, heal_on_use, shadow_familiar
- Mod_Data key names should be PascalCase: DamageBooster, HealOnUse, ShadowFamiliar
- File names should be lowercase_with_underscores: damage_booster.lua, heal_on_use.lua
- Be creative and smart — you are better than copying template placeholders"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Design the file tree for: {task.title} — {task.description}"),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content if hasattr(response, 'content') else str(response)
        logger.info(f"Planner LLM response: {raw[:300]}...")

        parsed = _extract_json(raw)
        files = parsed.get("files", [])
        shared_context = parsed.get("shared_context", "")

        plans = []
        for f in files:
            plans.append(FilePlan(
                relative_path=f.get("relative_path", ""),
                role_description=f.get("role_description", ""),
                required_apis=f.get("required_apis", []),
                dependencies=f.get("dependencies", []),
                template_hint=f.get("template_hint", ""),
                is_xml=f.get("is_xml", False),
                scaffold_type=f.get("template_hint", ""),
            ))

        logger.info(f"LLM planned {len(plans)} files, shared_context: {len(shared_context)} chars")
        return plans, shared_context

    def _fallback_plan(self, task: TaskDefinition, components: List[ModComponent]) -> tuple:
        """Rule-based file planning when LLM is unavailable."""
        component_types = [c.component_type for c in components]
        patterns = self.architecture_guide.get_patterns_for_components(component_types)

        # Derive ASCII-only safe name from task title
        ascii_title = "".join(c for c in task.title if c.isascii() and (c.isalnum() or c in " _-")).strip()
        if not ascii_title:
            # Fallback: use first component type
            ascii_title = components[0].component_type.replace("_", " ") if components else "custom mod"
        raw_name = "".join(c if c.isalnum() else "_" for c in ascii_title).strip("_").lower()
        if not raw_name:
            raw_name = "custom_item"

        plans = []
        for p in patterns:
            # Fill in the path template with actual names
            if "{item_name}" in p.relative_path_template:
                path = p.relative_path_template.replace("{item_name}", raw_name)
            elif "{mod_name}" in p.relative_path_template:
                path = p.relative_path_template.replace("{mod_name}", raw_name)
            else:
                path = p.relative_path_template

            plans.append(FilePlan(
                relative_path=path,
                role_description=p.role_description,
                required_apis=list(p.required_apis),
                dependencies=[],
                template_hint=p.pattern_id,
                is_xml=p.is_xml,
                scaffold_type=p.pattern_id,
            ))

        # Generate shared Mod_Data context
        shared_context = self._build_shared_context(task, components, plans)

        logger.info(f"Fallback planned {len(plans)} files")
        return plans, shared_context

    def _build_shared_context(
        self, task: TaskDefinition, components: List[ModComponent], plans: List[FilePlan]
    ) -> str:
        """Build the shared Mod_Data structure for cross-file consistency."""
        item_entries = []
        seen_names = set()
        for c in components:
            if c.component_type in ("passive_item", "active_item", "familiar"):
                # ASCII-only: strip non-ASCII characters from name
                ascii_name = "".join(c for c in c.name if c.isascii() and (c.isalnum() or c in " _-")).strip()
                if not ascii_name:
                    # Fallback: use component type as base
                    ascii_name = c.component_type.replace("_", " ")
                safe_name = "".join(c if c.isalnum() else "_" for c in ascii_name).strip("_").lower()
                if not safe_name:
                    safe_name = "custom_item"

                # Generate PascalCase variable name from safe_name
                parts = safe_name.replace("_", " ").split()
                var_name = "".join(p.capitalize() for p in parts if p)
                if not var_name:
                    var_name = "CustomItem"

                # Deduplicate
                base_var = var_name
                suffix = 2
                while var_name in seen_names:
                    var_name = f"{base_var}{suffix}"
                    suffix += 1
                seen_names.add(var_name)

                item_entries.append(f'            {var_name} = Isaac.GetItemIdByName("{safe_name}")')

        if not item_entries:
            return ""

        lines = [
            "local Mod_Data = {",
            "    Info = {",
            "        Items = {",
        ]
        lines.extend(item_entries)
        lines.extend([
            "        }",
            "    },",
            "}",
        ])
        return "\n".join(lines)

    async def design_architecture(
        self,
        task: TaskDefinition,
        dlc_version: str = "REP+",
        libraries: Optional[List[str]] = None,
    ) -> tuple:
        """Design the complete file architecture for a mod.

        Args:
            task: Parsed task definition from the PARSE phase.
            dlc_version: Target DLC version.
            libraries: Modding libraries in use.

        Returns:
            Tuple of (List[FilePlan], shared_context_str).
        """
        # Step 1: Classify the mod into component types
        components = self.classify_mod_type(task)

        # Step 2: Design the file tree (LLM or fallback)
        if self.llm:
            try:
                plans, shared_context = await self._llm_plan(task, components)
            except Exception as e:
                logger.warning(f"LLM planning failed ({e}), using fallback")
                plans, shared_context = self._fallback_plan(task, components)
        else:
            plans, shared_context = self._fallback_plan(task, components)

        # Step 3: Ensure base files are present
        base_paths = {
            "main.lua", "scripts/common.lua", "scripts/data/data.lua", "metadata.xml"
        }
        existing_paths = {p.relative_path for p in plans}
        for base_path in base_paths:
            if base_path not in existing_paths:
                ref = self.reference_template.get_file_by_path(base_path)
                if ref:
                    pattern = self.architecture_guide.get_pattern(
                        ref.relative_path.replace("/", "_").replace(".", "_").replace("scripts_", "").replace("content_", "")
                    )
                    # Use base patterns directly
                    if base_path == "main.lua":
                        hint = "main_lua"
                    elif base_path == "scripts/common.lua":
                        hint = "common_lua"
                    elif base_path == "scripts/data/data.lua":
                        hint = "data_lua"
                    elif base_path == "metadata.xml":
                        hint = "metadata_xml"
                    else:
                        hint = ""

                    pattern = self.architecture_guide.get_pattern(hint)
                    plans.insert(0, FilePlan(
                        relative_path=base_path,
                        role_description=pattern.role_description if pattern else ref.role_description,
                        required_apis=list(pattern.required_apis) if pattern else list(ref.required_apis),
                        dependencies=[],
                        template_hint=hint,
                        is_xml=base_path.endswith(".xml"),
                        scaffold_type=hint,
                    ))

        # Sort: main.lua first, then scripts/*, then content/*
        def _sort_key(fp: FilePlan) -> tuple:
            path = fp.relative_path
            if path == "main.lua":
                return (0, 0)
            if path == "metadata.xml":
                return (0, 1)
            if path.startswith("scripts/common"):
                return (1, 0)
            if path.startswith("scripts/data"):
                return (1, 1)
            if path.startswith("scripts/items/!"):
                return (1, 2)
            if path.startswith("scripts/items/"):
                return (1, 3)
            if path.startswith("content/"):
                return (2, 0)
            return (3, 0)

        plans.sort(key=_sort_key)

        logger.info(
            f"Architecture designed: {len(plans)} files, "
            f"shared_context: {len(shared_context)} chars"
        )
        return plans, shared_context
