"""
Parse docs/xml/*.md files into structured XmlFileSchema objects.

Each .md file documents one XML file type with attribute tables, sub-elements,
XML examples, and folder-placement rules (content/ vs resources/).
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger

from isaac_agent.core.state import XmlAttribute, XmlFileSchema, XmlSubElement


def _count_self_closing(block: str) -> int:
    """Count self-closing tags in an XML block."""
    return len(re.findall(r'<\w+\s+[^>]*/>', block))


_KNOWN_ROOT_TAGS = frozenset({
    "pocketitems", "items", "entities", "players", "costumes",
    "challenges", "sounds", "stages", "ItemPools", "babies",
    "bombcostumes", "bosscolors", "bossoverlays", "bosspools",
    "bossportraits", "curses", "cutscenes", "fortunes",
    "giantbook", "locusts", "minibosses", "nightmares", "wisps",
    "backdrops", "playerforms", "preload", "recipes", "rules",
    "seedmenu", "seeds", "translations", "achievements", "ambush",
    "music", "items_metadata", "fxlayers",
})


class XmlSchemaParser:
    """Parses docs/xml/*.md files into structured XmlFileSchema objects."""

    def __init__(self, docs_dir: Optional[str] = None, cache_path: Optional[str] = None):
        if docs_dir is None:
            docs_dir = str(Path(__file__).resolve().parent.parent.parent.parent / "docs" / "xml")
        self.docs_dir = Path(docs_dir)
        self.cache_path = Path(cache_path) if cache_path else None

    def parse_all(self) -> List[XmlFileSchema]:
        """Parse all .md files and return a list of XmlFileSchema objects."""
        if self.cache_path and self.cache_path.exists():
            cached = self._load_cache()
            if cached:
                return cached

        schemas = []
        for md_file in sorted(self.docs_dir.glob("*.md")):
            try:
                schema = self._parse_file(md_file)
                if schema:
                    schemas.append(schema)
            except Exception as e:
                logger.warning(f"Failed to parse {md_file.name}: {e}")

        logger.info(f"Parsed {len(schemas)} XML schemas from {len(list(self.docs_dir.glob('*.md')))} docs")

        if self.cache_path:
            self._save_cache(schemas)

        return schemas

    def _parse_file(self, path: Path) -> Optional[XmlFileSchema]:
        """Parse a single .md file into an XmlFileSchema."""
        text = path.read_text(encoding="utf-8")

        filename = self._extract_filename(text)
        if not filename:
            return None

        folder = self._detect_folder(text)
        root_element = self._extract_root_element(filename, text)
        root_attributes = self._extract_root_attributes(text)
        attributes = self._parse_attributes(text)
        sub_elements = self._parse_sub_elements(text)
        xml_examples = self._extract_xml_examples(text)
        tags = self._parse_tags(text)
        description = self._extract_description(text)

        return XmlFileSchema(
            filename=filename,
            root_element=root_element,
            root_attributes=root_attributes,
            folder=folder,
            attributes=attributes,
            sub_elements=sub_elements,
            tags=tags,
            xml_examples=xml_examples,
            description=description,
        )

    # ------------------------------------------------------------------
    # Filename extraction
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_filename(text: str) -> Optional[str]:
        m = re.search(r'# File "(.+?)"', text)
        if m:
            return m.group(1)
        m = re.search(r"# File '(.+?)'", text)
        if m:
            return m.group(1)
        return None

    # ------------------------------------------------------------------
    # Folder detection
    # ------------------------------------------------------------------

    @staticmethod
    def _detect_folder(text: str) -> str:
        content_green = False
        resource_green = False

        # Content folder
        cm = re.search(r'\*\*Content-Folder\*\*\{: \.xmlInfo \.green\}', text)
        if cm:
            content_green = True
        else:
            # Check if content folder is explicitly red or "has no effect"
            cr = re.search(
                r'\*\*Content-Folder\*\*\{: \.xmlInfo \.red\}|'
                r'content folder of a mod has no effect',
                text, re.IGNORECASE,
            )
            if not cr:
                # If not explicitly red and not green, check for "will add" or "is not tested yet"
                if re.search(r'content folder.*(?:will add|add new|add a new)', text, re.IGNORECASE):
                    content_green = True

        # Resource folder
        rm = re.search(r'\*\*Resource-Folder\*\*\{: \.xmlInfo \.green\}', text)
        if rm:
            resource_green = True

        if content_green and resource_green:
            return "both"
        if content_green:
            return "content"
        if resource_green:
            return "resources"

        # Known folder assignments (docs lacking explicit .green markers)
        _KNOWN_CONTENT = frozenset({
            "entities2.xml", "itempools.xml", "items_metadata.xml",
            "backdrops.xml", "playerforms.xml", "preload.xml",
            "achievements.xml", "ambush.xml", "music.xml",
        })
        filename_match = re.search(r'# File "(.+?)"', text)
        if filename_match and filename_match.group(1) in _KNOWN_CONTENT:
            return "content"

        return "unknown"

    # ------------------------------------------------------------------
    # Root element
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_root_element(filename: str, text: str) -> str:
        if filename == "pocketitems.xml":
            return "pocketitems"

        # Try to find root from full XML document examples first
        xml_blocks = re.findall(r'```xml\s*\n(.*?)\n```', text, re.DOTALL)
        for block in xml_blocks:
            root_m = re.search(r'<(\w+)[^>]*>', block)
            if root_m:
                tag = root_m.group(1)
                if tag in _KNOWN_ROOT_TAGS:
                    return tag

        # Second pass: accept any root element
        for block in xml_blocks:
            root_m = re.search(r'<(\w+)[^>]*>', block)
            if root_m:
                return root_m.group(1)

        # Derive from filename
        name = filename.replace(".xml", "")
        plural_map = {
            "babies": "babies", "challenges": "challenges",
            "bosspools": "bosspools", "bosscolors": "bosscolors",
            "bossportraits": "bossportraits", "seeds": "seeds",
            "fortunes": "fortunes", "locusts": "locusts",
            "minibosses": "minibosses", "nightmares": "nightmares",
            "wisps": "wisps", "curses": "curses", "cutscenes": "cutscenes",
            "entities2": "entities", "items": "items", "players": "players",
            "pocketitems": "pocketitems", "costumes2": "costumes",
            "itempools": "ItemPools", "sounds": "sounds", "stages": "stages",
            "backdrops": "backdrops", "bombcostumes": "bombcostumes",
            "bossoverlays": "bossoverlays", "giantbook": "giantbook",
            "items_metadata": "items_metadata", "playerforms": "playerforms",
            "preload": "preload", "recipes": "recipes", "rules": "rules",
            "seedmenu": "seedmenu", "translations": "translations",
            "achievements": "achievements", "ambush": "ambush", "music": "music",
        }
        return plural_map.get(name, name)

    @staticmethod
    def _extract_root_attributes(text: str) -> Dict[str, str]:
        """Extract attributes from the root element in XML examples."""
        attrs = {}
        xml_blocks = re.findall(r'```xml\s*\n(.*?)\n```', text, re.DOTALL)
        for block in xml_blocks:
            root_m = re.search(r'<(\w+)\s+([^>]+)>', block)
            if root_m:
                attr_str = root_m.group(2)
                for m in re.finditer(r'(\w+)="([^"]*)"', attr_str):
                    attrs[m.group(1)] = m.group(2)
                break
        return attrs

    # ------------------------------------------------------------------
    # Attributes table parsing
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_attributes(text: str) -> List[XmlAttribute]:
        """Parse the main attribute table."""
        attrs = []
        # Match "Variable Name" (space) or "Variable-Name" (hyphen)
        table_match = re.search(
            r'\| Variable[ -]Name \|.*?\n\|[:\- |]+\n((?:\|.+\n)+)',
            text, re.IGNORECASE,
        )
        if not table_match:
            return attrs

        rows_text = table_match.group(1)
        for row in rows_text.strip().split("\n"):
            attr = XmlSchemaParser._parse_table_row(row)
            if attr:
                attrs.append(attr)

        return attrs

    @staticmethod
    def _parse_table_row(row: str) -> Optional[XmlAttribute]:
        """Parse a single attribute table row."""
        cells = [c.strip() for c in row.split("|")[1:-1]]
        if len(cells) < 3:
            return None

        name = cells[0]
        raw_values = cells[1] if len(cells) > 1 else ""
        description = cells[2] if len(cells) > 2 else ""

        # Clean name — remove HTML, backticks, brackets
        name = re.sub(r'<[^>]+>', '', name)
        name = re.sub(r'[\[\]]', '', name).strip()

        if not name or name.lower() in ("variable-name", "variable name", "tag name"):
            return None

        # Determine type and possible values
        attr_type = "string"
        possible_values = []

        # Extract bracketed possible values from description (they may appear there too)
        search_text = f"{raw_values} {description}"
        pv_match = re.search(r'Possible values\s*:\s*\[([^\]]+)\]', search_text, re.IGNORECASE)
        if pv_match:
            vals = [v.strip().strip("'\"") for v in pv_match.group(1).split(",")]
            possible_values = [v for v in vals if v]

        # Detect type from value column hints
        rv_lower = raw_values.lower()
        if rv_lower in ("int", "integer"):
            attr_type = "int"
        elif rv_lower == "float":
            attr_type = "float"
        elif rv_lower in ("bool", "boolean"):
            attr_type = "bool"
        elif rv_lower in ("string", "str"):
            attr_type = "string"
        elif "string list" in rv_lower or "string list" in description.lower():
            attr_type = "string"
        elif possible_values:
            attr_type = "string"
        elif re.match(r'^\s*\d+\s*$', raw_values):
            attr_type = "int"

        # Detect required
        required = name.lower() in ("id", "name", "variant")

        # Clean description — remove markdown/HTML artifacts
        description = re.sub(r'<[^>]+>', '', description)
        description = re.sub(r'\{[^}]*\}', '', description).strip()

        return XmlAttribute(
            name=name,
            type=attr_type,
            possible_values=possible_values,
            description=description,
            required=required,
        )

    # ------------------------------------------------------------------
    # Sub-elements (nested tags)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_sub_elements(text: str) -> List[XmlSubElement]:
        """Parse nested child elements like <gibs>, <sample>, <card>, <pilleffect>."""
        sub_elements = []

        for pattern in [
            r'##\s+`<(\w+)>`',
            r'##\s+"(\w+)"\s+node',
        ]:
            for m in re.finditer(pattern, text):
                tag_name = m.group(1) or m.group(2)
                if tag_name in ("gibs", "sample", "card", "rune", "pilleffect",
                                "rule", "color", "item", "pool",
                                "challenge", "bomb", "costume", "sound",
                                "fx", "gfx"):
                    start = m.end()
                    chunk = text[start:start + 2000]
                    sub_attrs = XmlSchemaParser._parse_attributes(chunk)
                    if sub_attrs:
                        sub_elements.append(XmlSubElement(
                            name=tag_name,
                            attributes=sub_attrs,
                        ))

        # Remove duplicates by name
        seen = set()
        unique = []
        for se in sub_elements:
            if se.name not in seen:
                seen.add(se.name)
                unique.append(se)
        return unique

    # ------------------------------------------------------------------
    # XML examples
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_xml_examples(text: str) -> List[str]:
        examples = re.findall(r'```xml\s*\n(.*?)\n```', text, re.DOTALL)
        return [ex.strip() for ex in examples]

    # ------------------------------------------------------------------
    # Tags (for items.xml)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_tags(text: str) -> List[Dict[str, str]]:
        """Parse tag definitions (e.g., items.xml has a Tags Documentation table)."""
        tags = []
        tag_section = re.search(
            r'##\s+Tags?\s+Documentation.*?\n((?:\|.+\n)+)',
            text,
        )
        if not tag_section:
            return tags

        rows_text = tag_section.group(1)
        for row in rows_text.strip().split("\n"):
            cells = [c.strip() for c in row.split("|")[1:-1]]
            if len(cells) >= 2:
                tag_name = cells[0].strip()
                tag_desc = cells[1].strip()
                if tag_name and tag_name.lower() not in ("tag name", "variable-name"):
                    tags.append({"name": tag_name, "description": tag_desc})
        return tags

    # ------------------------------------------------------------------
    # Description
    # ------------------------------------------------------------------

    @staticmethod
    def _extract_description(text: str) -> str:
        """Extract the first descriptive paragraph after the heading."""
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("# ") and i + 1 < len(lines):
                desc_lines = []
                for j in range(i + 1, min(i + 5, len(lines))):
                    stripped = lines[j].strip()
                    if stripped and not stripped.startswith("#") and not stripped.startswith("|") \
                            and not stripped.startswith("[") and not stripped.startswith("**") \
                            and not stripped.startswith("old tutorial"):
                        desc_lines.append(re.sub(r'\{[^}]*\}', '', stripped).strip())
                if desc_lines:
                    return " ".join(desc_lines)
                break
        return ""

    # ------------------------------------------------------------------
    # Caching
    # ------------------------------------------------------------------

    def _save_cache(self, schemas: List[XmlFileSchema]) -> None:
        if not self.cache_path:
            return
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            data = []
            for s in schemas:
                data.append({
                    "filename": s.filename,
                    "root_element": s.root_element,
                    "root_attributes": s.root_attributes,
                    "folder": s.folder,
                    "attributes": [
                        {"name": a.name, "type": a.type,
                         "possible_values": a.possible_values,
                         "description": a.description, "required": a.required}
                        for a in s.attributes
                    ],
                    "sub_elements": [
                        {"name": se.name, "description": se.description,
                         "attributes": [
                             {"name": a.name, "type": a.type,
                              "possible_values": a.possible_values,
                              "description": a.description, "required": a.required}
                             for a in se.attributes
                         ]}
                        for se in s.sub_elements
                    ],
                    "tags": s.tags,
                    "xml_examples": s.xml_examples,
                    "description": s.description,
                })
            self.cache_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.info(f"Cached {len(data)} XML schemas to {self.cache_path}")
        except Exception as e:
            logger.warning(f"Failed to save schema cache: {e}")

    def _load_cache(self) -> Optional[List[XmlFileSchema]]:
        if not self.cache_path or not self.cache_path.exists():
            return None
        try:
            cache_mtime = self.cache_path.stat().st_mtime
            for md_file in self.docs_dir.glob("*.md"):
                if md_file.stat().st_mtime > cache_mtime:
                    logger.info("XML schema cache is stale, re-parsing")
                    return None

            data = json.loads(self.cache_path.read_text(encoding="utf-8"))
            schemas = []
            for entry in data:
                schemas.append(XmlFileSchema(
                    filename=entry["filename"],
                    root_element=entry["root_element"],
                    root_attributes=entry.get("root_attributes", {}),
                    folder=entry["folder"],
                    attributes=[XmlAttribute(**a) for a in entry["attributes"]],
                    sub_elements=[
                        XmlSubElement(
                            name=se["name"],
                            description=se.get("description", ""),
                            attributes=[XmlAttribute(**a) for a in se["attributes"]],
                        )
                        for se in entry.get("sub_elements", [])
                    ],
                    tags=entry.get("tags", []),
                    xml_examples=entry.get("xml_examples", []),
                    description=entry.get("description", ""),
                ))
            logger.info(f"Loaded {len(schemas)} XML schemas from cache")
            return schemas
        except Exception as e:
            logger.warning(f"Failed to load schema cache: {e}")
            return None
