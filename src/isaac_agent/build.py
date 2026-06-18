"""
Mod artifact builder for the Isaac AI Agent.

Packages generated Lua code into a proper TBOI: Repentance mod structure
ready for deployment to the game's mods directory.
"""

import shutil
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from loguru import logger

from isaac_agent.core.state import GeneratedCode, GeneratedXml
from isaac_agent.core.agent import MainAgent


def _indent_xml(elem: ET.Element, level: int = 0) -> None:
    """Pretty-print XML elements with indentation."""
    indent = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            _indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent


class ModBuilder:
    """Builds a deployable mod folder from generated Lua code artifacts.

    If an agent is provided, it will use the agent's detected mods directory
    so that built mods go directly into the game's mods folder.
    """

    def __init__(self, output_dir: Optional[str] = None, agent: Optional["MainAgent"] = None):
        """
        Args:
            output_dir: Root directory for built mods. If None, tries to use
                        the agent's detected mods dir, then falls back to ./build.
            agent: Optional MainAgent reference for path detection.
        """
        if output_dir:
            self.output_dir = Path(output_dir)
        elif agent is not None and agent.mods_dir and agent.mods_dir.exists():
            self.output_dir = agent.mods_dir
            logger.info(f"ModBuilder using detected mods dir: {self.output_dir}")
        else:
            from isaac_agent.tools.isaac_path_resolver import find_isaac_mods_dir
            detected = find_isaac_mods_dir()
            if detected:
                self.output_dir = detected
                logger.info(f"ModBuilder using auto-detected mods dir: {self.output_dir}")
            else:
                self.output_dir = Path("build")
                logger.info(f"ModBuilder using default output: {self.output_dir}")

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build(
        self,
        artifacts: List[GeneratedCode],
        mod_name: str = "isaac_mod",
        mod_id: int = 1,
        mod_version: str = "1.0.0",
        mod_description: str = "",
        session_id: str = "",
        clean: bool = True,
        xml_artifacts: Optional[List[GeneratedXml]] = None,
    ) -> Path:
        """
        Build a complete multi-file mod folder from generated code artifacts.

        Produces a directory structure matching the gold-standard Isaac mod layout:

            build/<mod_name>/
            ├── main.lua
            ├── metadata.xml
            ├── content/
            │   └── items.xml
            ├── scripts/
            │   ├── common.lua
            │   ├── data/
            │   │   └── data.lua
            │   └── items/
            │       ├── !items.lua
            │       ├── item1.lua
            │       └── item2.lua
            └── resources/
                └── gfx/

        If artifacts have file_path set (multi-file mode), each artifact is
        written to its planned path. Otherwise falls back to single main.lua.
        """
        mod_dir = self.output_dir / mod_name

        if clean and mod_dir.exists():
            shutil.rmtree(mod_dir)
            logger.info(f"Cleaned existing build: {mod_dir}")

        mod_dir.mkdir(parents=True, exist_ok=True)

        # Check if we have multi-file artifacts (architecture-first mode)
        has_file_paths = any(getattr(a, "file_path", "") for a in artifacts)

        if has_file_paths:
            # Multi-file mode: write each artifact to its planned path
            for artifact in artifacts:
                if not artifact.file_path:
                    continue
                file_path = mod_dir / artifact.file_path
                file_path.parent.mkdir(parents=True, exist_ok=True)

                if artifact.lua_code:
                    file_path.write_text(artifact.lua_code, encoding="utf-8")
                    logger.info(f"Wrote {artifact.file_path} ({len(artifact.lua_code)} chars)")
                else:
                    file_path.touch()
                    logger.info(f"Created empty {artifact.file_path} (placeholder)")
        else:
            # Legacy flat mode: combine all into main.lua for backward compat
            main_lua_path = mod_dir / "main.lua"
            combined_lua = self._combine_lua(artifacts, mod_name, session_id)
            main_lua_path.write_text(combined_lua, encoding="utf-8")
            logger.info(f"Wrote main.lua ({len(combined_lua)} chars) [legacy flat mode]")

        # Ensure base directories exist
        (mod_dir / "content").mkdir(parents=True, exist_ok=True)
        (mod_dir / "resources" / "gfx").mkdir(parents=True, exist_ok=True)
        (mod_dir / "resources" / "gfx" / ".gitkeep").touch()

        # Write metadata.xml
        metadata_path = mod_dir / "metadata.xml"
        metadata_xml = self._build_metadata(mod_name, mod_id, mod_version, mod_description)
        metadata_path.write_text(metadata_xml, encoding="utf-8")
        logger.info("Wrote metadata.xml")

        # Write XML files from the generation stage
        if xml_artifacts:
            for gen_xml in xml_artifacts:
                if not gen_xml.entries:
                    continue

                folder = gen_xml.folder if gen_xml.folder not in ("unknown",) else "content"
                target_dir = mod_dir / folder
                target_dir.mkdir(parents=True, exist_ok=True)
                xml_path = target_dir / gen_xml.xml_file

                xml_str = self._build_xml_file(gen_xml, mod_name)
                xml_path.write_text(xml_str, encoding="utf-8")
                logger.info(f"Wrote {gen_xml.xml_file} ({len(gen_xml.entries)} entries) to {folder}/")

        logger.info(f"Mod built: {mod_dir}")
        return mod_dir

    def build_from_agent_result(
        self,
        result,
        mod_name: str = "isaac_mod",
        clean: bool = True,
    ) -> Path:
        """Build a mod from a completed agent workflow result.

        Supports both multi-file (architecture-first) and legacy flat modes.
        """
        if isinstance(result, dict):
            artifacts = result.get("generated_code", [])
            session_id = result.get("session_id", "")
            task = result.get("task")
            description = task.description if task else ""
            xml_artifacts = result.get("generated_xml", [])
        else:
            artifacts = result.generated_code
            session_id = result.session_id
            description = result.task.description if result.task else ""
            xml_artifacts = getattr(result, "generated_xml", [])

        return self.build(
            artifacts=artifacts,
            mod_name=mod_name,
            mod_description=description,
            session_id=session_id,
            clean=clean,
            xml_artifacts=xml_artifacts if xml_artifacts else None,
        )

    @staticmethod
    def _combine_lua(
        artifacts: List[GeneratedCode],
        mod_name: str,
        session_id: str,
    ) -> str:
        """DEPRECATED: Combine all Lua artifacts into a single main.lua file.

        Only used for legacy flat mode when artifacts lack file_path.
        """
        header = f"""-- =============================================================================
-- {mod_name}
-- Generated by Isaac AI Agent
-- Session: {session_id}
-- Date: {datetime.now().isoformat()}
-- =============================================================================

local mod = RegisterMod("{mod_name}", 1)
local game = Game()

"""
        parts = [header]
        for i, artifact in enumerate(artifacts):
            parts.append(f"-- [{artifact.scaffold_type}]")
            parts.append(artifact.lua_code)
            if i < len(artifacts) - 1:
                parts.append("")

        return "\n".join(parts) + "\n"

    @staticmethod
    def _build_metadata(
        mod_name: str,
        mod_id: int,
        mod_version: str,
        mod_description: str,
    ) -> str:
        """Generate metadata.xml for the mod."""
        root = ET.Element("metadata")
        ET.SubElement(root, "name").text = mod_name
        ET.SubElement(root, "id").text = str(mod_id)
        ET.SubElement(root, "version").text = mod_version
        ET.SubElement(root, "description").text = mod_description or "Generated by Isaac AI Agent"
        ET.SubElement(root, "author").text = "Isaac AI Agent"
        ET.SubElement(root, "directory").text = mod_name

        _indent_xml(root)
        return ET.tostring(root, encoding="unicode", xml_declaration=True)

    @staticmethod
    def _build_xml_file(gen_xml: GeneratedXml, mod_name: str) -> str:
        """Serialize a GeneratedXml to a properly formatted XML string."""
        schema = gen_xml.xml_file.replace(".xml", "")
        root_el = ET.Element(schema)

        for entry in gen_xml.entries:
            child = ET.SubElement(root_el, entry.element_tag)
            for attr_name, attr_value in entry.attributes.items():
                child.set(attr_name, str(attr_value))
            for sub in entry.sub_elements:
                sub_el = ET.SubElement(child, sub.element_tag)
                for sattr, sval in sub.attributes.items():
                    sub_el.set(sattr, str(sval))

        _indent_xml(root_el)
        return ET.tostring(root_el, encoding="unicode", xml_declaration=True)

    def list_builds(self) -> List[Path]:
        """List all built mod directories."""
        if not self.output_dir.exists():
            return []
        return sorted(
            p for p in self.output_dir.iterdir()
            if p.is_dir() and not p.name.startswith(".")
        )


def main() -> None:
    """Entry point for python -m isaac_agent.build

    Builds a sample mod to demonstrate the output structure.
    """
    import asyncio

    logger.info("Running mod build demonstration...")

    agent = MainAgent()
    builder = ModBuilder()

    async def _run_demo() -> None:
        prompts = [
            "create a custom item that gives the player health when used",
            "make a room modifier that spawns extra pickups on room clear",
        ]

        for prompt in prompts:
            logger.info(f"Generating mod from: '{prompt}'")
            result = await agent.run(prompt)

            # Derive a safe mod name from the task title
            if isinstance(result, dict):
                title = result.get("task", {}).get("title", "untitled")
            else:
                title = result.task.title if result.task else "untitled"
            safe_name = "".join(c if c.isalnum() else "_" for c in title).strip("_").lower()

            mod_path = builder.build_from_agent_result(result, mod_name=safe_name)

            print(f"\n  Built mod at: {mod_path.resolve()}")
            print(f"  Structure:")
            for f in sorted(mod_path.rglob("*")):
                if f.is_file():
                    rel = f.relative_to(mod_path)
                    print(f"    {rel}")

    asyncio.run(_run_demo())


if __name__ == "__main__":
    main()
