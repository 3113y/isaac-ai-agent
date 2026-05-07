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

from isaac_agent.core.state import GeneratedCode
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
    ) -> Path:
        """
        Build a complete mod folder from generated code artifacts.

        Produces a directory structure compatible with TBOI: Repentance:

            build/<mod_name>/
            ├── main.lua
            ├── metadata.xml
            ├── content/
            │   └── items.xml
            └── resources/
                └── gfx/

        Args:
            artifacts: GeneratedCode objects from the agent workflow.
            mod_name: Name of the mod (used as directory name).
            mod_id: Numeric mod ID for the game.
            mod_version: Semver version string.
            mod_description: Description for metadata.xml.
            session_id: Workflow session ID for provenance tracking.
            clean: If True, remove existing build directory first.

        Returns:
            Path to the built mod directory.
        """
        mod_dir = self.output_dir / mod_name

        if clean and mod_dir.exists():
            shutil.rmtree(mod_dir)
            logger.info(f"Cleaned existing build: {mod_dir}")

        # Create directory structure
        mod_dir.mkdir(parents=True, exist_ok=True)
        content_dir = mod_dir / "content"
        resources_dir = mod_dir / "resources" / "gfx"
        content_dir.mkdir(parents=True, exist_ok=True)
        resources_dir.mkdir(parents=True, exist_ok=True)

        # Write main.lua — combine all artifacts
        main_lua_path = mod_dir / "main.lua"
        combined_lua = self._combine_lua(artifacts, mod_name, session_id)
        main_lua_path.write_text(combined_lua, encoding="utf-8")
        logger.info(f"Wrote main.lua ({len(combined_lua)} chars)")

        # Write metadata.xml
        metadata_path = mod_dir / "metadata.xml"
        metadata_xml = self._build_metadata(mod_name, mod_id, mod_version, mod_description)
        metadata_path.write_text(metadata_xml, encoding="utf-8")
        logger.info(f"Wrote metadata.xml")

        # Write items.xml if CUSTOM_ITEM artifacts exist
        item_artifacts = [a for a in artifacts if a.scaffold_type == "CUSTOM_ITEM"]
        if item_artifacts:
            items_xml_path = content_dir / "items.xml"
            items_xml = self._build_items_xml(item_artifacts, mod_name)
            items_xml_path.write_text(items_xml, encoding="utf-8")
            logger.info(f"Wrote items.xml ({len(item_artifacts)} items)")

        # Place a .gitkeep in resources/gfx/
        (resources_dir / ".gitkeep").touch()

        logger.info(f"Mod built: {mod_dir}")
        return mod_dir

    def build_from_agent_result(
        self,
        result,
        mod_name: str = "isaac_mod",
        clean: bool = True,
    ) -> Path:
        """Build a mod from a completed agent workflow result.

        Args:
            result: AgentState (or dict from ainvoke) with generated_code.
            mod_name: Name of the mod.
            clean: If True, remove existing build directory first.

        Returns:
            Path to the built mod directory.
        """
        if isinstance(result, dict):
            artifacts = result.get("generated_code", [])
            session_id = result.get("session_id", "")
            task = result.get("task")
            description = task.description if task else ""
        else:
            artifacts = result.generated_code
            session_id = result.session_id
            description = result.task.description if result.task else ""

        return self.build(
            artifacts=artifacts,
            mod_name=mod_name,
            mod_description=description,
            session_id=session_id,
            clean=clean,
        )

    @staticmethod
    def _combine_lua(
        artifacts: List[GeneratedCode],
        mod_name: str,
        session_id: str,
    ) -> str:
        """Combine all Lua artifacts into a single main.lua file."""
        header = f"""-- =============================================================================
-- {mod_name}
-- Generated by Isaac AI Agent
-- Session: {session_id}
-- Date: {datetime.now().isoformat()}
-- =============================================================================

local mod = RegisterMod("{mod_name}", 1)
local game = Game()
local json = require("json")

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
    def _build_items_xml(
        item_artifacts: List[GeneratedCode],
        mod_name: str,
    ) -> str:
        """Generate items.xml with placeholder entries for custom items."""
        root = ET.Element("items")
        root.set("mod", mod_name)

        for i, artifact in enumerate(item_artifacts):
            item = ET.SubElement(root, "item")
            item.set("id", str(1000 + i))
            item.set("name", f"{mod_name}_item_{i}")
            item.set("type", "active")
            item.set("description", artifact.scaffold_type)
            item.set("gfx", f"gfx/ui/items/{mod_name}_item_{i}.png")

        _indent_xml(root)
        return ET.tostring(root, encoding="unicode", xml_declaration=True)

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
