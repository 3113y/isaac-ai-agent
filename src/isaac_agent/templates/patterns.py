"""
Architectural patterns for Isaac mod file generation.

Replaces the rigid fill-in-the-blank templates in lua_skeletons.py with
descriptive patterns that guide the LLM on HOW to structure each file type
without constraining WHAT code to write.

Each FilePattern describes a file's role, required APIs, callback conventions,
include chain position, and provides a reference example for few-shot prompting.

IMPORTANT: All names in reference_code (Item1, item1, etc.) are INTENTIONAL
PLACEHOLDERS. The LLM MUST replace them with names derived from the user's request.
See ReferenceTemplate.naming_example_section() for the transformation example.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FilePattern:
    """Architectural pattern for a specific file role in an Isaac mod."""
    pattern_id: str                                # e.g., "passive_item_script"
    relative_path_template: str                    # e.g., "scripts/items/{item_name}.lua"
    role_description: str                          # What this file does in the mod
    required_apis: List[str] = field(default_factory=list)
    callback_patterns: List[str] = field(default_factory=list)
    reference_code: str = ""                       # Canonical example for few-shot (uses PLACEHOLDER names)
    include_chain_position: str = ""               # Where this file sits in the include chain
    sibling_patterns: List[str] = field(default_factory=list)
    is_base_file: bool = False                     # True for always-required files
    is_xml: bool = False


class ModArchitectureGuide:
    """Guides the agent on how to structure mod files based on architectural patterns.

    Replaces the old LuaTemplateManager. Instead of fill-in-the-blank templates,
    this provides architectural knowledge that the LLM uses to generate properly
    structured code for each file independently.
    """

    PATTERNS = {
        "main_lua": FilePattern(
            pattern_id="main_lua",
            relative_path_template="main.lua",
            role_description="Entry point: registers the mod with RegisterMod and includes scripts/common.lua. This file should be minimal — just registration and the include statement.",
            required_apis=["RegisterMod"],
            callback_patterns=[],
            reference_code='local mod = RegisterMod("{mod_name}", 1)\ninclude("scripts.common")',
            include_chain_position="root (first file loaded)",
            sibling_patterns=[],
            is_base_file=True,
            is_xml=False,
        ),
        "common_lua": FilePattern(
            pattern_id="common_lua",
            relative_path_template="scripts/common.lua",
            role_description="Top-level aggregator: includes data/data.lua and items/!items.lua. This is the central include hub that loads all mod scripts.",
            required_apis=[],
            callback_patterns=[],
            reference_code='include("scripts.data.data")\ninclude("scripts.items.!items")',
            include_chain_position="included by main.lua",
            sibling_patterns=["data_lua", "items_init_lua"],
            is_base_file=True,
            is_xml=False,
        ),
        "data_lua": FilePattern(
            pattern_id="data_lua",
            relative_path_template="scripts/data/data.lua",
            role_description="Mod_Data centralized structure: stores all item/entity IDs using Isaac.GetItemIdByName(). Every item script references this structure for cross-file consistency. REPLACE Item1/item1 with names derived from user's request.",
            required_apis=["Isaac.GetItemIdByName"],
            callback_patterns=[],
            reference_code='local Mod_Data = {\n    Info = {\n        Items = {\n            Item1 = Isaac.GetItemIdByName("item1")\n        }\n    },\n}',
            include_chain_position="included by common.lua",
            sibling_patterns=[],
            is_base_file=True,
            is_xml=False,
        ),
        "items_init_lua": FilePattern(
            pattern_id="items_init_lua",
            relative_path_template="scripts/items/!items.lua",
            role_description="Item init aggregator: includes all individual item script files. Each item gets its own include() line. REPLACE item1/item2 with actual file names.",
            required_apis=[],
            callback_patterns=[],
            reference_code='include("scripts.items.item1")\ninclude("scripts.items.item2")',
            include_chain_position="included by common.lua",
            sibling_patterns=[],
            is_base_file=False,
            is_xml=False,
        ),
        "passive_item_script": FilePattern(
            pattern_id="passive_item_script",
            relative_path_template="scripts/items/{item_name}.lua",
            role_description="Passive item callback script: uses MC_POST_EVALUATE_CACHE to apply persistent stat effects. Iterates all players with HasCollectible() check. REPLACE Item1/item1/passive_function1 with names derived from user's request.",
            required_apis=["HasCollectible", "ModCallbacks.MC_POST_EVALUATE_CACHE", "Isaac.GetPlayer", "Game.GetNumPlayers"],
            callback_patterns=["MC_POST_EVALUATE_CACHE"],
            reference_code='function mod:passive_function1()\n    for i = 0, Game():GetNumPlayers() - 1 do\n        local player = Isaac.GetPlayer(i)\n        if player:HasCollectible(Mod_Data.Info.Items.Item1) then\n            local damage = player.Damage\n            player.Damage = damage * 2\n        end\n    end\nend\nmod:AddCallback(ModCallbacks.MC_POST_EVALUATE_CACHE, mod.passive_function1)',
            include_chain_position="included by !items.lua",
            sibling_patterns=["active_item_script", "familiar_script"],
            is_base_file=False,
            is_xml=False,
        ),
        "active_item_script": FilePattern(
            pattern_id="active_item_script",
            relative_path_template="scripts/items/{item_name}.lua",
            role_description="Active item callback script: uses MC_USE_ITEM with signature (_, rng, player). Checks HasCollectible() for the item. The callback is registered with the specific item ID as third argument to AddCallback. REPLACE Item2/item2/active_function1 with names derived from user's request.",
            required_apis=["HasCollectible", "ModCallbacks.MC_USE_ITEM"],
            callback_patterns=["MC_USE_ITEM"],
            reference_code='function mod:active_function1(_, rng, player)\n    if player:HasCollectible(Mod_Data.Info.Items.Item2) then\n        -- active item effect\n    end\nend\nmod:AddCallback(ModCallbacks.MC_USE_ITEM, mod.active_function1, Mod_Data.Info.Items.Item2)',
            include_chain_position="included by !items.lua",
            sibling_patterns=["passive_item_script", "familiar_script"],
            is_base_file=False,
            is_xml=False,
        ),
        "familiar_script": FilePattern(
            pattern_id="familiar_script",
            relative_path_template="scripts/items/{item_name}.lua",
            role_description="Familiar companion script: uses three callbacks — MC_FAMILIAR_INIT (setup), MC_FAMILIAR_UPDATE (per-frame logic), MC_PRE_TEAR_COLLISION (tear collision handling). REPLACE familiar_function1 with descriptive function names.",
            required_apis=["ModCallbacks.MC_FAMILIAR_INIT", "ModCallbacks.MC_FAMILIAR_UPDATE", "ModCallbacks.MC_PRE_TEAR_COLLISION"],
            callback_patterns=["MC_FAMILIAR_INIT", "MC_FAMILIAR_UPDATE", "MC_PRE_TEAR_COLLISION"],
            reference_code='function mod:familiar_init()\n    -- init logic\nend\nmod:AddCallback(ModCallbacks.MC_FAMILIAR_INIT, mod.familiar_init)\n\nfunction mod:familiar_update()\n    -- update logic\nend\nmod:AddCallback(ModCallbacks.MC_FAMILIAR_UPDATE, mod.familiar_update)\n\nfunction mod:familiar_collision()\n    -- collision logic\nend\nmod:AddCallback(ModCallbacks.MC_PRE_TEAR_COLLISION, mod.familiar_collision)',
            include_chain_position="included by !items.lua",
            sibling_patterns=["passive_item_script", "active_item_script"],
            is_base_file=False,
            is_xml=False,
        ),
        "items_xml": FilePattern(
            pattern_id="items_xml",
            relative_path_template="content/items.xml",
            role_description="Item XML definitions: defines all items with id, name, description, gfx animation, quality, and type-specific attributes (maxcharges for active, cache for passive/familiar).",
            required_apis=[],
            callback_patterns=[],
            reference_code='<items gfxroot="gfx/items" version="1">\n  <passive id="1" name="item name" description="item desc" gfx="items.anm2" cache="damage" quality="2"/>\n</items>',
            include_chain_position="N/A (XML file, not in Lua include chain)",
            sibling_patterns=[],
            is_base_file=False,
            is_xml=True,
        ),
        "metadata_xml": FilePattern(
            pattern_id="metadata_xml",
            relative_path_template="metadata.xml",
            role_description="Mod metadata: name, id, version, description for the game's mod manager.",
            required_apis=[],
            callback_patterns=[],
            reference_code='<?xml version="1.0" encoding="utf-8"?>\n<metadata>\n  <name>{mod_name}</name>\n  <id></id>\n  <version></version>\n  <description></description>\n</metadata>',
            include_chain_position="N/A (XML file)",
            sibling_patterns=[],
            is_base_file=True,
            is_xml=True,
        ),
    }

    # Maps component types to the pattern IDs they need
    COMPONENT_TO_PATTERNS = {
        "passive_item": ["main_lua", "common_lua", "data_lua", "items_init_lua", "passive_item_script", "items_xml", "metadata_xml"],
        "active_item": ["main_lua", "common_lua", "data_lua", "items_init_lua", "active_item_script", "items_xml", "metadata_xml"],
        "familiar": ["main_lua", "common_lua", "data_lua", "items_init_lua", "familiar_script", "items_xml", "metadata_xml"],
    }

    def get_pattern(self, pattern_id: str) -> Optional[FilePattern]:
        """Get a single pattern by ID."""
        return self.PATTERNS.get(pattern_id)

    def get_base_patterns(self) -> List[FilePattern]:
        """Return always-required base patterns (main.lua, common.lua, data.lua, metadata)."""
        return [p for p in self.PATTERNS.values() if p.is_base_file]

    def get_patterns_for_component(self, component_type: str) -> List[FilePattern]:
        """Return all patterns needed for a given mod component."""
        pattern_ids = self.COMPONENT_TO_PATTERNS.get(component_type, [])
        return [self.PATTERNS[pid] for pid in pattern_ids if pid in self.PATTERNS]

    def get_patterns_for_components(self, component_types: List[str]) -> List[FilePattern]:
        """Return deduplicated patterns needed for multiple component types."""
        seen = set()
        patterns = []
        # Always include base patterns
        for p in self.get_base_patterns():
            if p.pattern_id not in seen:
                seen.add(p.pattern_id)
                patterns.append(p)
        # Add component-specific patterns
        for ct in component_types:
            for p in self.get_patterns_for_component(ct):
                if p.pattern_id not in seen:
                    seen.add(p.pattern_id)
                    patterns.append(p)
        return patterns

    def as_prompt_context(self, patterns: List[FilePattern]) -> str:
        """Format selected patterns as a prompt injection for file generation.

        Provides the architectural context for generating a specific file:
        its role, required APIs, callback conventions, and a reference example.
        """
        lines = [
            "=== ARCHITECTURAL PATTERNS FOR THIS FILE ===",
            "The reference code below shows the CORRECT STRUCTURE and PATTERN.",
            "IMPORTANT: item1/Item1/passive_function1 are FORMAT PLACEHOLDERS.",
            "You MUST replace them with descriptive names derived from the user's request.",
            "See the naming rules in the system prompt for how to derive real names.",
        ]
        for p in patterns:
            lines.append(f"\nPattern: {p.pattern_id}")
            lines.append(f"Path: {p.relative_path_template}")
            lines.append(f"Role: {p.role_description}")
            lines.append(f"Position in include chain: {p.include_chain_position}")
            if p.required_apis:
                lines.append(f"Required APIs: {', '.join(p.required_apis)}")
            if p.callback_patterns:
                lines.append(f"Callback conventions: {', '.join(p.callback_patterns)}")
            if p.reference_code:
                lines.append(f"Reference example:\n```lua\n{p.reference_code}\n```")
        return "\n".join(lines)

    def list_patterns(self) -> List[str]:
        """List all pattern IDs."""
        return list(self.PATTERNS.keys())
