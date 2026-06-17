"""
Maps Lua scaffold types to required XML files for Isaac mods.

Each scaffold type (CUSTOM_ITEM, CUSTOM_ENTITY, etc.) has a set of XML files
that must be generated alongside the Lua code. Some are always required;
others are conditional, triggered by keywords in the task description.
"""

from typing import List, Dict

# Core scaffold-to-XML mapping
SCAFFOLD_XML_MAP: Dict[str, List[dict]] = {
    "MOD_INIT": [],
    "MC_POST_GAME_STARTED": [],
    "EVENT_HANDLER": [],
    "ROOM_MODIFIER": [],
    "CUSTOM_ITEM": [
        {"xml_file": "items.xml", "folder": "content", "required": True},
        {"xml_file": "costumes2.xml", "folder": "content", "required": False,
         "condition": "has_costume"},
        {"xml_file": "itempools.xml", "folder": "content", "required": False,
         "condition": "add_to_pools"},
        {"xml_file": "pocketitems.xml", "folder": "content", "required": False,
         "condition": "is_pocket_item"},
    ],
    # New architecture patterns (planner.py + patterns.py)
    "passive_item_script": [
        {"xml_file": "items.xml", "folder": "content", "required": True},
        {"xml_file": "costumes2.xml", "folder": "content", "required": False,
         "condition": "has_costume"},
        {"xml_file": "itempools.xml", "folder": "content", "required": False,
         "condition": "add_to_pools"},
        {"xml_file": "pocketitems.xml", "folder": "content", "required": False,
         "condition": "is_pocket_item"},
    ],
    "active_item_script": [
        {"xml_file": "items.xml", "folder": "content", "required": True},
        {"xml_file": "costumes2.xml", "folder": "content", "required": False,
         "condition": "has_costume"},
        {"xml_file": "itempools.xml", "folder": "content", "required": False,
         "condition": "add_to_pools"},
        {"xml_file": "pocketitems.xml", "folder": "content", "required": False,
         "condition": "is_pocket_item"},
    ],
    "familiar_script": [
        {"xml_file": "items.xml", "folder": "content", "required": True},
        {"xml_file": "costumes2.xml", "folder": "content", "required": False,
         "condition": "has_costume"},
    ],
    "items_xml": [
        {"xml_file": "items.xml", "folder": "content", "required": True},
    ],
    "items_init_lua": [
        {"xml_file": "items.xml", "folder": "content", "required": True},
    ],
    "CUSTOM_ENTITY": [
        {"xml_file": "entities2.xml", "folder": "content", "required": True},
    ],
    "PLAYER_MODIFIER": [
        {"xml_file": "players.xml", "folder": "content", "required": True},
    ],
}

# Keywords that trigger conditional XML files
CONDITION_KEYWORDS: Dict[str, List[str]] = {
    "has_costume": ["costume", "appearance", "visual", "sprite", "look", "outfit"],
    "add_to_pools": ["item pool", "treasure room", "shop pool", "boss pool", "devil room"],
    "is_pocket_item": ["card", "rune", "pill", "pocket", "consumable", "tarot", "soul stone"],
}


def resolve_xml_files(
    scaffolds: List[str],
    task_description: str = "",
    lua_code: str = "",
) -> List[dict]:
    """
    Determine which XML files need to be generated given the scaffold types
    and task context.

    Args:
        scaffolds: List of scaffold type names (e.g., ["CUSTOM_ITEM"]).
        task_description: The task description for keyword matching.
        lua_code: The generated Lua code for additional keyword matching.

    Returns:
        List of dicts, each with xml_file, folder, and required keys.
    """
    combined_text = f"{task_description} {lua_code}".lower()
    result = []
    seen = set()

    for scaffold in scaffolds:
        mappings = SCAFFOLD_XML_MAP.get(scaffold, [])
        for mapping in mappings:
            key = mapping["xml_file"]
            if key in seen:
                continue

            if mapping.get("required", False):
                result.append({
                    "xml_file": mapping["xml_file"],
                    "folder": mapping["folder"],
                    "required": True,
                })
                seen.add(key)
            elif "condition" in mapping:
                cond = mapping["condition"]
                keywords = CONDITION_KEYWORDS.get(cond, [])
                if any(kw in combined_text for kw in keywords):
                    result.append({
                        "xml_file": mapping["xml_file"],
                        "folder": mapping["folder"],
                        "required": False,
                    })
                    seen.add(key)

    return result
