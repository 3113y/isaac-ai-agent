"""
Lua template scaffolds for Isaac mod generation
"""

from typing import Dict, List, Optional
from loguru import logger


class LuaTemplateManager:
    """
    Manages Lua code templates and scaffolds for Isaac mods

    Provides pre-built code structures for common patterns:
    - Mod initialization
    - Event callbacks
    - Entity manipulation
    - Item/Enemy customization
    """

    # Core template library
    TEMPLATES = {
        "MOD_INIT": """-- =============================================================================
-- Mod Initialization Template
-- =============================================================================

local mod = RegisterMod("%(mod_name)s", 1)

-- Mod metadata
local modVersion = "1.0.0"

-- Initialize mod
function mod:OnStart()
    logger:info("%(mod_name)s initialized")
end

-- Main update loop
function mod:OnUpdate()
    -- Update logic goes here
end

-- Cleanup
function mod:OnExit()
    logger:info("%(mod_name)s exited")
end

return mod
""",
        "MC_POST_GAME_STARTED": """-- =============================================================================
-- Post Game Started Callback
-- =============================================================================

function mod:MC_POST_GAME_STARTED(continued)
    if continued then
        logger:info("Game continued from save")
    else
        logger:info("New game started")
    end
    
    local game = Game()
    local player = game:GetPlayer(0)
    
    -- Initialize game logic
    -- Setup custom items, enemies, etc.
end

mod:AddCallback(ModCallbacks.MC_POST_GAME_STARTED, 
    function(continued) 
        mod.MC_POST_GAME_STARTED(continued) 
    end
)
""",
        "CUSTOM_ITEM": """-- =============================================================================
-- Custom Item Template
-- =============================================================================

local itemID = Isaac.GetItemIdByName("%(item_name)s")

function mod:OnItemPickup(item, player)
    if item.ID == itemID then
        -- Item pickup logic
        logger:info("Picked up %(item_name)s")
    end
end

function mod:OnItemUse(item, player)
    if item.ID == itemID then
        -- Item activation logic
        logger:info("Used %(item_name)s")
    end
end

mod:AddCallback(ModCallbacks.MC_PRE_PICKUP_COLLISION,
    function(entity)
        mod:OnItemPickup(entity.Item, Isaac.GetPlayer(0))
    end
)
""",
        "CUSTOM_ENTITY": """-- =============================================================================
-- Custom Entity Template
-- =============================================================================

local entityType = Isaac.GetEntityTypeByName("%(entity_name)s")

function mod:OnEntityInit(entity)
    if entity.Type == entityType then
        entity:ClearEntityFlags(EntityFlag.FLAG_APPEAR)
        logger:info("Custom entity spawned: %(entity_name)s")
    end
end

function mod:OnEntityUpdate(entity)
    if entity.Type == entityType then
        -- Update custom entity
    end
end

function mod:OnEntityDeath(entity)
    if entity.Type == entityType then
        logger:info("Custom entity died: %(entity_name)s")
    end
end

mod:AddCallback(ModCallbacks.MC_POST_ENTITY_INIT, 
    function(entity) mod:OnEntityInit(entity) end
)
mod:AddCallback(ModCallbacks.MC_POST_ENTITY_UPDATE,
    function(entity) mod:OnEntityUpdate(entity) end
)
""",
        "EVENT_HANDLER": """-- =============================================================================
-- Event Handler Template
-- =============================================================================

local events = {}

function events:Register(eventName, callback)
    if not self[eventName] then
        self[eventName] = {}
    end
    table.insert(self[eventName], callback)
end

function events:Dispatch(eventName, ...)
    if self[eventName] then
        for _, callback in ipairs(self[eventName]) do
            callback(...)
        end
    end
end

-- Usage:
-- events:Register("player_damaged", function(player, damage)
--     logger:info("Player took damage: " .. damage)
-- end)

return events
""",
        "ROOM_MODIFIER": """-- =============================================================================
-- Room Modifier Template
-- =============================================================================

function mod:OnNewRoom()
    local room = Game():GetRoom()
    local roomType = room:GetType()
    
    logger:info("Entered room type: " .. roomType)
    
    -- Modify room properties
    -- Add custom obstacles, enemies, etc.
end

function mod:OnRoomClear()
    local room = Game():GetRoom()
    logger:info("Room cleared")
    
    -- Add rewards, spawn entities, etc.
end

mod:AddCallback(ModCallbacks.MC_POST_NEW_ROOM, 
    function() mod:OnNewRoom() end
)
mod:AddCallback(ModCallbacks.MC_POST_ROOM_CLEAR,
    function() mod:OnRoomClear() end
)
""",
        "PLAYER_MODIFIER": """-- =============================================================================
-- Player Modifier Template
-- =============================================================================

function mod:OnPlayerInit(player)
    logger:info("Player initialized: " .. player:GetName())
    
    -- Add starting items
    -- Modify starting stats
end

function mod:OnPlayerTakeDamage(player, damage)
    logger:info("Player took " .. damage .. " damage")
    
    -- Apply damage modifiers
    -- Trigger special effects
end

function mod:OnPlayerUpdate(player)
    -- Per-frame player logic
end

mod:AddCallback(ModCallbacks.MC_POST_PLAYER_INIT,
    function(player) mod:OnPlayerInit(player) end
)
mod:AddCallback(ModCallbacks.MC_ENTITY_TAKE_DMG,
    function(entity, damage) 
        if entity:IsPlayer() then
            mod:OnPlayerTakeDamage(entity, damage)
        end
    end
)
""",
    }

    def __init__(self):
        """Initialize template manager (DEPRECATED — use ModArchitectureGuide instead)."""
        logger.warning(
            "LuaTemplateManager is DEPRECATED. Use ModArchitectureGuide + ReferenceTemplate "
            "from isaac_agent.templates.patterns and isaac_agent.templates.reference_template "
            "for the new architecture-first workflow."
        )
        logger.info(f"📋 LuaTemplateManager initialized with {len(self.TEMPLATES)} templates (legacy)")

    def get_template(self, scaffold_type: str, **kwargs) -> str:
        """
        Get a template and optionally format it with parameters

        Args:
            scaffold_type: Type of scaffold (e.g., "MC_POST_GAME_STARTED")
            **kwargs: Parameters for string formatting

        Returns:
            Formatted Lua code template
        """
        if scaffold_type not in self.TEMPLATES:
            logger.warning(f"⚠️  Template '{scaffold_type}' not found")
            return self._get_generic_template(scaffold_type)

        template = self.TEMPLATES[scaffold_type]

        # Apply formatting if parameters provided
        if kwargs:
            try:
                return template % kwargs
            except KeyError as e:
                logger.warning(f"⚠️  Missing template parameter: {e}")
                return template

        return template

    def find_templates(self, query: str) -> List[str]:
        """
        Find templates matching a query

        Args:
            query: Search query (e.g., "item", "entity")

        Returns:
            List of matching template names
        """
        query_lower = query.lower()
        matches = [name for name in self.TEMPLATES.keys() if query_lower in name.lower()]

        logger.info(f"🔎 Found {len(matches)} templates for '{query}'")
        return matches

    def list_templates(self) -> List[str]:
        """List all available templates"""
        return list(self.TEMPLATES.keys())

    def get_template_description(self, scaffold_type: str) -> str:
        """Get description of a template"""
        descriptions = {
            "MOD_INIT": "基础 Mod 初始化和注册",
            "MC_POST_GAME_STARTED": "游戏开始后事件处理器",
            "CUSTOM_ITEM": "自定义道具创建模板",
            "CUSTOM_ENTITY": "自定义实体/敌人模板",
            "EVENT_HANDLER": "事件分发系统",
            "ROOM_MODIFIER": "房间修改钩子",
            "PLAYER_MODIFIER": "玩家修改和属性",
        }
        return descriptions.get(scaffold_type, "暂无描述")

    def _get_generic_template(self, scaffold_type: str) -> str:
        """Generate a generic template for unknown scaffold types"""
        return f"""-- =============================================================================
-- {scaffold_type} Handler
-- =============================================================================

function mod:{scaffold_type}(...)
    -- TODO: Implement {scaffold_type} logic
    logger:info("{scaffold_type} called")
end

-- Register callback
mod:AddCallback(ModCallbacks.{scaffold_type},
    function(...) mod:{scaffold_type}(...) end
)
"""

    def validate_template(self, scaffold_type: str) -> bool:
        """Check if a template exists"""
        return scaffold_type in self.TEMPLATES

    def export_templates(self) -> Dict[str, str]:
        """Export all templates"""
        return self.TEMPLATES.copy()

    def add_custom_template(self, name: str, template: str) -> None:
        """
        Add a custom template

        Args:
            name: Template name
            template: Template Lua code string
        """
        self.TEMPLATES[name] = template
        logger.info(f"✅ Custom template added: {name}")

    def get_template_stats(self) -> Dict[str, int]:
        """Get statistics about templates"""
        return {
            "total_templates": len(self.TEMPLATES),
            "total_lines": sum(t.count("\n") for t in self.TEMPLATES.values()),
            "categories": len(set(name.split("_")[0] for name in self.TEMPLATES.keys())),
        }
