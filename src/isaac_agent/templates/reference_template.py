"""
Gold-standard Isaac mod reference template.

Encodes the canonical project structure from 项目总结.md as structured
knowledge that the planning phase uses to design mod file trees.

IMPORTANT: All names in template_code (item1, Item1, etc.) are INTENTIONAL
PLACEHOLDERS. They demonstrate the STRUCTURE and PATTERN — the LLM MUST
replace them with descriptive names derived from the user's actual request.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ReferenceFile:
    """A single file from the reference mod template."""
    relative_path: str                              # e.g., "scripts/items/item1.lua"
    role_description: str                           # What this file does
    required_apis: List[str] = field(default_factory=list)
    template_code: str = ""                         # Reference code for few-shot prompting
    is_entry_point: bool = False                    # Is this main.lua?
    include_chain_after: Optional[str] = None       # Included after which file
    mod_component_types: List[str] = field(default_factory=list)  # passive_item, active_item, etc.


class ReferenceTemplate:
    """Structured representation of the gold-standard Isaac mod template.

    Parses the canonical project structure from 项目总结.md into programmatic
    data used by the planner (level B: system prompt) and file generator
    (level C: few-shot examples).
    """

    FILES: List[ReferenceFile] = [
        ReferenceFile(
            relative_path="main.lua",
            role_description="Entry point: registers the mod with RegisterMod and includes scripts/common.lua",
            required_apis=["RegisterMod"],
            template_code='local mod = RegisterMod("{mod_name}", 1)\ninclude("scripts.common")',
            is_entry_point=True,
            include_chain_after=None,
            mod_component_types=[],
        ),
        ReferenceFile(
            relative_path="metadata.xml",
            role_description="Mod metadata: name, id, version, description",
            required_apis=[],
            template_code='<?xml version="1.0" encoding="utf-8"?>\n<metadata>\n  <name>{mod_name}</name>\n  <id></id>\n  <version></version>\n  <description></description>\n</metadata>',
            is_entry_point=False,
            include_chain_after=None,
            mod_component_types=[],
        ),
        ReferenceFile(
            relative_path="scripts/common.lua",
            role_description="Aggregator: includes data/data.lua and items/!items.lua to load all scripts",
            required_apis=[],
            template_code='include("scripts.data.data")\ninclude("scripts.items.!items")',
            is_entry_point=False,
            include_chain_after="main.lua",
            mod_component_types=[],
        ),
        ReferenceFile(
            relative_path="scripts/data/data.lua",
            role_description="Mod_Data centralized structure storing item/entity IDs from Isaac.GetItemIdByName",
            required_apis=["Isaac.GetItemIdByName"],
            template_code='local Mod_Data = {\n    Info = {\n        Items = {\n            Item1 = Isaac.GetItemIdByName("item1"),\n            Item2 = Isaac.GetItemIdByName("item2"),\n            Item3 = Isaac.GetItemIdByName("item3")\n        }\n    },\n}',
            is_entry_point=False,
            include_chain_after="scripts/common.lua",
            mod_component_types=[],
        ),
        ReferenceFile(
            relative_path="scripts/items/!items.lua",
            role_description="Item init aggregator: includes all individual item script files",
            required_apis=[],
            template_code='include("scripts.items.item1")\ninclude("scripts.items.item2")\ninclude("scripts.items.item3")',
            is_entry_point=False,
            include_chain_after="scripts/data/data.lua",
            mod_component_types=[],
        ),
        ReferenceFile(
            relative_path="scripts/items/item1.lua",
            role_description="Passive item: uses MC_POST_EVALUATE_CACHE callback, applies effect when player has the collectible",
            required_apis=["HasCollectible", "ModCallbacks.MC_POST_EVALUATE_CACHE", "Isaac.GetPlayer", "Game.GetNumPlayers"],
            template_code='function mod:passive_function1()\n    for i = 0, Game():GetNumPlayers() - 1 do\n        local player = Isaac.GetPlayer(i)\n        if player:HasCollectible(Mod_Data.Info.Items.Item1) then\n            local damage = player.Damage\n            player.Damage = damage * 2\n        end\n    end\nend\nmod:AddCallback(ModCallbacks.MC_POST_EVALUATE_CACHE, mod.passive_function1)',
            is_entry_point=False,
            include_chain_after="scripts/items/!items.lua",
            mod_component_types=["passive_item"],
        ),
        ReferenceFile(
            relative_path="scripts/items/item2.lua",
            role_description="Active item: uses MC_USE_ITEM callback with (_, rng, player) signature, triggered when player uses the item",
            required_apis=["HasCollectible", "ModCallbacks.MC_USE_ITEM"],
            template_code='function mod:active_function1(_, rng, player)\n    if player:HasCollectible(Mod_Data.Info.Items.Item2) then\n        -- active item effect code here\n    end\nend\nmod:AddCallback(ModCallbacks.MC_USE_ITEM, mod.active_function1, Mod_Data.Info.Items.Item2)',
            is_entry_point=False,
            include_chain_after="scripts/items/!items.lua",
            mod_component_types=["active_item"],
        ),
        ReferenceFile(
            relative_path="scripts/items/item3.lua",
            role_description="Familiar item: uses MC_FAMILIAR_INIT, MC_FAMILIAR_UPDATE, MC_PRE_TEAR_COLLISION callbacks",
            required_apis=["ModCallbacks.MC_FAMILIAR_INIT", "ModCallbacks.MC_FAMILIAR_UPDATE", "ModCallbacks.MC_PRE_TEAR_COLLISION"],
            template_code='function mod:familiar_function1()\n    -- init logic\nend\nmod:AddCallback(ModCallbacks.MC_FAMILIAR_INIT, mod.familiar_function1)\n\nfunction mod:familiar_function2()\n    -- update logic\nend\nmod:AddCallback(ModCallbacks.MC_FAMILIAR_UPDATE, mod.familiar_function2)\n\nfunction mod:familiar_function3()\n    -- collision logic\nend\nmod:AddCallback(ModCallbacks.MC_PRE_TEAR_COLLISION, mod.familiar_function3)',
            is_entry_point=False,
            include_chain_after="scripts/items/!items.lua",
            mod_component_types=["familiar"],
        ),
        ReferenceFile(
            relative_path="content/items.xml",
            role_description="Item XML definitions with attributes: id, name, description, gfx, quality, tags, etc.",
            required_apis=[],
            template_code='<items gfxroot="gfx/items" version="1">\n    <active id="1" name="active item" description="active item desc" gfx="active items.anm2" maxcharges="6" quality="2"/>\n    <passive id="2" name="passive item" description="passive item desc" gfx="passive items.anm2" cache="damage" quality="2"/>\n    <familiar id="3" name="familiar item" description="familiar desc" gfx="familiar items.anm2" quality="2"/>\n</items>',
            is_entry_point=False,
            include_chain_after=None,
            mod_component_types=["passive_item", "active_item", "familiar"],
        ),
    ]

    # Component-type to required file mapping
    COMPONENT_FILES = {
        "passive_item": [
            "main.lua",
            "metadata.xml",
            "scripts/common.lua",
            "scripts/data/data.lua",
            "scripts/items/!items.lua",
            "scripts/items/item1.lua",
            "content/items.xml",
        ],
        "active_item": [
            "main.lua",
            "metadata.xml",
            "scripts/common.lua",
            "scripts/data/data.lua",
            "scripts/items/!items.lua",
            "scripts/items/item2.lua",
            "content/items.xml",
        ],
        "familiar": [
            "main.lua",
            "metadata.xml",
            "scripts/common.lua",
            "scripts/data/data.lua",
            "scripts/items/!items.lua",
            "scripts/items/item3.lua",
            "content/items.xml",
        ],
    }

    def get_files_for_component(self, component_type: str) -> List[ReferenceFile]:
        """Return all reference files relevant to a given component type."""
        target_paths = self.COMPONENT_FILES.get(component_type, [])
        return [f for f in self.FILES if f.relative_path in target_paths]

    def get_always_required_files(self) -> List[ReferenceFile]:
        """Return files always needed regardless of component type."""
        always = {"main.lua", "metadata.xml", "scripts/common.lua", "scripts/data/data.lua"}
        return [f for f in self.FILES if f.relative_path in always]

    def get_include_chain(self) -> List[str]:
        """Return the ordered include chain showing file loading order."""
        return [
            "main.lua",
            "scripts/common.lua",
            "scripts/data/data.lua",
            "scripts/items/!items.lua",
            "scripts/items/item1.lua",
            "scripts/items/item2.lua",
            "scripts/items/item3.lua",
        ]

    def get_file_by_path(self, relative_path: str) -> Optional[ReferenceFile]:
        """Look up a reference file by its relative path."""
        for f in self.FILES:
            if f.relative_path == relative_path:
                return f
        return None

    @staticmethod
    def naming_example_section() -> str:
        """Return a concrete naming transformation example for the prompt.

        This is the KEY section that shows the LLM HOW to go from a user request
        to real, descriptive names. Without this, the LLM copies placeholders.
        """
        return """=== NAMING: HOW TO DERIVE REAL NAMES FROM USER REQUEST ===

The names item1/item2/Item1/Item2 in the template above are FORMAT PLACEHOLDERS.
You MUST replace them with descriptive English names derived from the user's request.

CONCRETE EXAMPLE — user asks: "一个翻倍伤害的被动道具" (a passive item that doubles damage)

  WRONG (copying placeholders):
    file: scripts/items/item1.lua
    Mod_Data key: Item1
    function: passive_function1
    ItemIdByName: "item1"

  RIGHT (derived from the user's actual request):
    file: scripts/items/damage_multiplier.lua
    Mod_Data key: DamageMultiplier
    function: damage_multiplier_effect
    ItemIdByName: "damage_multiplier"

NAMING CONVENTIONS:
  - File names: lowercase_with_underscores (damage_multiplier.lua, heal_on_use.lua)
  - Mod_Data keys: PascalCase (DamageMultiplier, HealOnUse, ShadowFamiliar)
  - Functions: lowercase_with_underscores + _effect/_init/_update suffix
  - ItemIdByName string: matches file name (lowercase_with_underscores)
  - ALL must be ASCII English ONLY — translate Chinese requests to English

HOW TO DERIVE NAMES:
  1. Read the user's request carefully — what does the item DO?
  2. Describe the item's FUNCTION in 2-4 English words
  3. Convert to naming convention: "doubles damage" → damage_multiplier / DamageMultiplier
  4. "heals when used" → heal_on_use / HealOnUse
  5. "a shadow companion" → shadow_familiar / ShadowFamiliar
  6. "gives speed boost" → speed_boost / SpeedBoost
  7. "shoots fire tears" → fire_tears / FireTears

You are SMARTER than copying placeholders. Be creative. Think about what the user asked for."""

    def as_prompt_context(self) -> str:
        """Format the entire reference structure as a system prompt string.

        Used by the PLAN phase to show the LLM the gold-standard mod layout.
        """
        lines = [
            "=== GOLD-STANDARD ISAAC MOD TEMPLATE ===",
            "The following structure represents the standard, well-architected",
            "Isaac mod layout. Design your file tree to conform to this pattern:",
            "",
            "Directory structure:",
            "  ref/",
            "    main.lua              # Entry point: RegisterMod + include('scripts.common')",
            "    metadata.xml          # Mod metadata (name, id, version, description)",
            "    content/",
            "      items.xml           # Item definitions (<passive>, <active>, or <familiar> tags)",
            "    scripts/",
            "      common.lua          # Aggregator: includes data.lua and !items.lua",
            "      data/",
            "        data.lua          # Mod_Data structure storing item/entity IDs",
            "      items/",
            "        !items.lua        # Item init aggregator: includes all item scripts",
            "        [item_name].lua   # Per-item script files (passive/active/familiar)",
            "",
            "Include chain (load order):",
            "  main.lua -> scripts/common.lua -> scripts/data/data.lua",
            "                                     -> scripts/items/!items.lua",
            "                                           -> scripts/items/[item_name].lua",
            "",
            "Key patterns:",
            "- Mod_Data is the centralized data structure storing all item/entity IDs",
            "- Each item type gets its own file under scripts/items/",
            "- !items.lua is the aggregator that includes all individual item scripts",
            "- common.lua is the top-level aggregator",
            "- main.lua only contains RegisterMod and include('scripts.common')",
            "- Item files use Mod_Data.Info.Items.ItemName for cross-file consistency",
            "",
            self.naming_example_section(),
        ]
        return "\n".join(lines)

    def as_few_shot(self, relative_path: str) -> str:
        """Return the reference code for a specific file as a few-shot example."""
        ref = self.get_file_by_path(relative_path)
        if ref and ref.template_code:
            return (
                f"-- Reference PATTERN for {relative_path}:\n"
                f"-- Role: {ref.role_description}\n"
                f"-- NOTE: item1/Item1 are PLACEHOLDERS. Replace with names derived from user's request.\n"
                f"{ref.template_code}"
            )
        return ""
