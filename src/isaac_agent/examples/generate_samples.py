"""
Generate sample Isaac mods demonstrating the agent's capabilities.

This module uses the agent's template system to produce sample mods
and outputs them via the ModBuilder to show the folder structure.
"""

import asyncio
from loguru import logger

from isaac_agent.core.agent import MainAgent
from isaac_agent.build import ModBuilder


SAMPLE_PROMPTS = [
    (
        "health_on_clear",
        "Give the player one full heart of health every time they clear a room",
    ),
    (
        "custom_explosive_item",
        "Create a custom active item called 'Megablast' that spawns a large explosion "
        "at the player's position when used",
    ),
    (
        "speed_boost_entity",
        "Create a custom enemy called 'Speed Demon' that moves 2x faster than normal enemies "
        "and explodes on death",
    ),
    (
        "starter_kit",
        "Give the player 5 coins, 1 bomb, and 1 key at the start of every new game",
    ),
]


async def generate_all_samples(output_dir: str = "build") -> None:
    """Generate all sample mods and print their folder structures.

    Args:
        output_dir: Root directory for built mods.
    """
    agent = MainAgent()
    builder = ModBuilder(output_dir=output_dir)

    print("\n" + "=" * 70)
    print("  Isaac AI Agent — Sample Mod Generation")
    print("=" * 70)

    for mod_slug, prompt in SAMPLE_PROMPTS:
        print(f"\n{'─' * 70}")
        print(f"  Sample: {mod_slug}")
        print(f"  Prompt: \"{prompt}\"")
        print(f"{'─' * 70}")

        result = await agent.run(prompt)

        if isinstance(result, dict):
            session_id = result.get("session_id", "?")
            artifacts = result.get("generated_code", [])
        else:
            session_id = result.session_id
            artifacts = result.generated_code

        print(f"  Session: {session_id}")
        print(f"  Artifacts generated: {len(artifacts)}")
        for a in artifacts:
            code_preview = a.lua_code[:120].replace("\n", "\\n")
            print(f"    - {a.scaffold_type}: {code_preview}...")

        mod_path = builder.build_from_agent_result(
            result,
            mod_name=mod_slug,
            clean=True,
        )

        print(f"\n  Output folder structure:")
        _print_tree(mod_path)

    # Summary
    print(f"\n{'═' * 70}")
    print(f"  All builds in: {builder.output_dir.resolve()}")
    all_builds = builder.list_builds()
    print(f"  Total mods built: {len(all_builds)}")
    for b in all_builds:
        print(f"    {b.name}/")
    print(f"{'═' * 70}\n")


def _print_tree(path, prefix: str = "") -> None:
    """Print a directory tree."""
    items = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        connector = "  └── " if is_last else "  ├── "
        if item.is_dir():
            print(f"{prefix}{connector}{item.name}/")
            _print_tree(item, prefix + ("     " if is_last else "  │   "))
        else:
            size = item.stat().st_size
            size_str = f" ({size}B)" if size < 1024 else f" ({size // 1024}KB)"
            print(f"{prefix}{connector}{item.name}{size_str}")


def main() -> None:
    """Entry point for python -m isaac_agent.examples.generate_samples."""
    asyncio.run(generate_all_samples())


if __name__ == "__main__":
    main()
