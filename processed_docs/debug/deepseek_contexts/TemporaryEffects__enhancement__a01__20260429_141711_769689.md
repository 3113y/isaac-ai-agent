# DeepSeek Context

- class: TemporaryEffects
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T14:17:11.769824

## Prompt

```text
你是《以撒的结合》API 文档分析助手，请严格输出 JSON。

规则：
1. 当前请求只对应一个类/对象，不要跨类推断。
2. 同一个类的全部方法在同一上下文中统一分析，避免重复和错乱。
3. 先输出类级总结，再输出每个方法的独立总结。
4. method_id 必须与输入一致，不可新增、不可遗漏。
5. 输出必须是 JSON 对象，禁止输出 markdown 代码块和额外解释。

返回格式：
{
  "class_enhancement": {
    "summary": "类整体作用总结",
    "use_cases": ["用途1", "用途2"],
    "key_methods": ["关键方法1", "关键方法2"]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "该方法的独立总结",
      "use_cases": ["该方法用途1", "该方法用途2"],
      "key_methods": ["相关方法或调用点"]
    }
  ]
}

额外要求：
- class_enhancement.key_methods 只能引用当前类中的方法名。
- 每个 method_enhancement.summary 必须针对对应 method_id，禁止复用同一段文本。
- 每个 method_enhancement.key_methods 的第一个元素必须是该 method_id 对应的方法名。
- use_cases 和 key_methods 每项尽量简洁，最多 5 项。

类名：TemporaryEffects

原始 md 文档（该类完整文档，可能已截断）：
# Class "TemporaryEffects"

???+ info
    You can get this class by using the following function:

    * [EntityPlayer:GetEffects()](EntityPlayer.md#geteffects)

    ???+ example "Example Code"
        ```lua
        local player = Isaac.GetPlayer()
        local tempEffects = player:GetEffects()
        ```

## Functions
### Add·Collectible·Effect () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddCollectibleEffect ( [CollectibleType](enums/CollectibleType.md) CollectibleType, boolean AddCostume = true, int Count = 1 ) {: .copyable aria-label='Functions' }
Adds the CollectibleEffect associated with a given item. If the passed item's CollectibleEffect is marked to have a cooldown or be persistent in items.xml, this will be respected.

???+ info "Misinformation"
    TemporaryEffects, despite their names, are not and were never intended to be fake or temporary copies of items. Notably every single active item automatically grants its CollectibleEffect on use, and this is often closely tied to its effect; CollectibleEffects can therefore be visuallised more as an item's state. For example in passive items:

    * Holy Mantle utilises its CollectibleEffect to track how many shield charges the player currently has.
    * Most familiar items can have their familiar granted via their CollectibleEffect.
    * Whore of Babylon and Crown of Light grant their CollectibleEffects while activated.

    Some items can have their effects granted invisibly through the use of their CollectibleEffect, oftentimes this is because another item pre-repentance wished to invoke its effect (such as Monster Manual). Many post-repentance items use real fake copies of items for this purpose, but adding these is not supported by the API and some such as Hemoptysis and Berserk! still use CollectibleEffects for their cooldowns. You should not assume that any given item will work as a TemporaryEffect the same as it does when actually obtained.

    ???- info "Supported Items"
        Passive items with notable CollectibleEffects (excluding quest items).

        --8<-- "docs/snippets/AddCollectibleEffect.txt"

???- example "Example Code"
    This code applies the effect and costume of the item "Sad Onion" to the player.

    ```lua
    local player = Isaac.GetPlayer()
    player:GetEffects():AddCollectibleEffect(CollectibleType.COLLECTIBLE_SAD_ONION, true)
    ```
___
### Add·Null·Effect () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddNullEffect ( [NullItemID](enums/NullItemID.md) NullId, boolean AddCostume = true, int Count = 1 ) {: .copyable aria-label='Functions' }

___
### Add·Trinket·Effect () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddTrinketEffect ( [TrinketType](enums/TrinketType.md) TrinketType, boolean AddCostume = true, int Count = 1 ) {: .copyable aria-label='Functions' }

___
### Clear·Effects () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void ClearEffects ( ) {: .copyable aria-label='Functions' }

___
### Get·Collectible·Effect () {: aria-label='Functions' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [TemporaryEffect](TemporaryEffect.md) GetCollectibleEffect ( [CollectibleType](enums/CollectibleType.md) CollectibleType ) {: .copyable aria-label='Functions' }

___
### Get·Collectible·Effect·Num () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### int GetCollectibleEffectNum ( [CollectibleType](enums/CollectibleType.md) CollectibleType ) {: .copyable aria-label='Functions' }

___
### Get·Effects·List () {: aria-label='Functions' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [EffectList](CppContainer_Vector_EffectList.md) GetEffectsList ( ) {: .copyable aria-label='Functions' }

___
### Get·Null·Effect () {: aria-label='Functions' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [TemporaryEffect](TemporaryEffect.md) GetNullEffect ( [ItemConfigNullItemID](ItemConfig_Item.md) NullId ) {: .copyable aria-label='Functions' }

___
### Get·Null·Effect·Num () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### int GetNullEffectNum ( [ItemConfigNullItemID](ItemConfig_Item.md) NullId ) {: .copyable aria-label='Functions' }

___
### Get·Trinket·Effect () {: aria-label='Functions' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [TemporaryEffect](TemporaryEffect.md) GetTrinketEffect ( [TrinketType](enums/TrinketType.md) TrinketType ) {: .copyable aria-label='Functions' }

___
### Get·Trinket·Effect·Num () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### int GetTrinketEffectNum ( [TrinketType](enums/TrinketType.md) TrinketType ) {: .copyable aria-label='Functions' }

___
### Has·Collectible·Effect () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean HasCollectibleEffect ( [CollectibleType](enums/CollectibleType.md) CollectibleType ) {: .copyable aria-label='Functions' }

___
### Has·Null·Effect () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean HasNullEffect ( [ItemConfigNullItemID](ItemConfig_Item.md) NullId ) {: .copyable aria-label='Functions' }

___
### Has·Trinket·Effect () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean HasTrinketEffect ( [TrinketType](enums/TrinketType.md) TrinketType ) {: .copyable aria-label='Functions' }

___
### Remove·Collectible·Effect () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void RemoveCollectibleEffect ( [CollectibleType](enums/CollectibleType.md) CollectibleType, int Count = 1 ) {: .copyable aria-label='Functions' }
Count = -1 removes all instances of the effect
___
### Remove·Null·Effect () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void RemoveNullEffect ( [ItemConfigNullItemID](ItemConfig_Item.md) NullId, int Count = 1 ) {: .copyable aria-label='Functions' }
Count = -1 removes all instances of the effect
___
### Remove·Trinket·Effect () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void RemoveTrinketEffect ( [TrinketType](enums/TrinketType.md) TrinketType, int Count = 1 ) {: .copyable aria-label='Functions' }
Count = -1 removes all instances of the effect
___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "AddCollectibleEffect",
    "signature": "void AddCollectibleEffect ( [CollectibleType](enums/CollectibleType.md) CollectibleType, boolean AddCostume = true, int Count = 1 ) {: .copyable aria-label='Functions' }",
    "description": "Adds the CollectibleEffect associated with a given item. If the passed item's CollectibleEffect is marked to have a cooldown or be persistent in items.xml, this will be respected."
  },
  {
    "method_id": "m002",
    "name": "AddNullEffect",
    "signature": "void AddNullEffect ( [NullItemID](enums/NullItemID.md) NullId, boolean AddCostume = true, int Count = 1 ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "AddTrinketEffect",
    "signature": "void AddTrinketEffect ( [TrinketType](enums/TrinketType.md) TrinketType, boolean AddCostume = true, int Count = 1 ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "ClearEffects",
    "signature": "void ClearEffects ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "GetCollectibleEffect",
    "signature": "const [TemporaryEffect](TemporaryEffect.md) GetCollectibleEffect ( [CollectibleType](enums/CollectibleType.md) CollectibleType ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "GetCollectibleEffectNum",
    "signature": "int GetCollectibleEffectNum ( [CollectibleType](enums/CollectibleType.md) CollectibleType ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "GetEffectsList",
    "signature": "const [EffectList](CppContainer_Vector_EffectList.md) GetEffectsList ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "GetNullEffect",
    "signature": "const [TemporaryEffect](TemporaryEffect.md) GetNullEffect ( [ItemConfigNullItemID](ItemConfig_Item.md) NullId ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "GetNullEffectNum",
    "signature": "int GetNullEffectNum ( [ItemConfigNullItemID](ItemConfig_Item.md) NullId ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "GetTrinketEffect",
    "signature": "const [TemporaryEffect](TemporaryEffect.md) GetTrinketEffect ( [TrinketType](enums/TrinketType.md) TrinketType ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "GetTrinketEffectNum",
    "signature": "int GetTrinketEffectNum ( [TrinketType](enums/TrinketType.md) TrinketType ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "HasCollectibleEffect",
    "signature": "boolean HasCollectibleEffect ( [CollectibleType](enums/CollectibleType.md) CollectibleType ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "HasNullEffect",
    "signature": "boolean HasNullEffect ( [ItemConfigNullItemID](ItemConfig_Item.md) NullId ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "HasTrinketEffect",
    "signature": "boolean HasTrinketEffect ( [TrinketType](enums/TrinketType.md) TrinketType ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "RemoveCollectibleEffect",
    "signature": "void RemoveCollectibleEffect ( [CollectibleType](enums/CollectibleType.md) CollectibleType, int Count = 1 ) {: .copyable aria-label='Functions' }",
    "description": "Count = -1 removes all instances of the effect"
  },
  {
    "method_id": "m016",
    "name": "RemoveNullEffect",
    "signature": "void RemoveNullEffect ( [ItemConfigNullItemID](ItemConfig_Item.md) NullId, int Count = 1 ) {: .copyable aria-label='Functions' }",
    "description": "Count = -1 removes all instances of the effect"
  },
  {
    "method_id": "m017",
    "name": "RemoveTrinketEffect",
    "signature": "void RemoveTrinketEffect ( [TrinketType](enums/TrinketType.md) TrinketType, int Count = 1 ) {: .copyable aria-label='Functions' }",
    "description": "Count = -1 removes all instances of the effect"
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "管理玩家身上的临时效果，包括道具效果(CollectibleEffect)、空物品效果(NullEffect)和饰品效果(TrinketEffect)。这些效果主要用于追踪物品内部状态（如神圣屏障层数）而非提供完整的物品能力。",
    "use_cases": [
      "跟踪特定物品的冷却或激活状态",
      "临时赋予物品关联的装饰或状态效果",
      "在需要无实际物品时模拟物品的部分行为"
    ],
    "key_methods": [
      "AddCollectibleEffect",
      "RemoveCollectibleEffect",
      "HasCollectibleEffect",
      "GetCollectibleEffect",
      "ClearEffects"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "添加指定道具的CollectibleEffect，可附加角色服装，并遵循物品的冷却或持久标记。",
      "use_cases": [
        "赋予玩家神圣屏障的充能层数",
        "触发需要物品状态支持的效果而不实际获得道具",
        "为特定道具显示其装饰服装"
      ],
      "key_methods": [
        "AddCollectibleEffect",
        "GetCollectibleEffect",
        "HasCollectibleEffect",
        "RemoveCollectibleEffect"
      ]
    },
    {
      "method_id": "m002",
      "summary": "添加指定空物品的NullEffect，可附加服装和设置叠加数量。",
      "use_cases": [
        "给予空卡片或符文等效果",
        "叠加空物品的装饰状态"
      ],
      "key_methods": [
        "AddNullEffect",
        "GetNullEffect",
        "HasNullEffect",
        "RemoveNullEffect"
      ]
    },
    {
      "method_id": "m003",
      "summary": "添加指定饰品的TrinketEffect，可附加服装和设置叠加数量。",
      "use_cases": [
        "临时赋予饰品效果及其服装",
        "测试饰品相关状态"
      ],
      "key_methods": [
        "AddTrinketEffect",
        "GetTrinketEffect",
        "HasTrinketEffect",
        "RemoveTrinketEffect"
      ]
    },
    {
      "method_id": "m004",
      "summary": "移除玩家当前所有的临时效果，包括道具效果、空物品效果和饰品效果。",
      "use_cases": [
        "重置所有临时赋予的状态",
        "清理不需要的效果时使用"
      ],
      "key_methods": [
        "ClearEffects",
        "RemoveCollectibleEffect",
        "RemoveNullEffect",
        "RemoveTrinketEffect"
      ]
    },
    {
      "method_id": "m005",
      "summary": "获取指定道具类型的TemporaryEffect对象，用于读取该效果的详细状态。",
      "use_cases": [
        "查询特定道具效果的内部数据",
        "判断效果是否处于激活或冷却状态"
      ],
      "key_methods": [
        "GetCollectibleEffect",
        "GetCollectibleEffectNum",
        "HasCollectibleEffect"
      ]
    },
    {
      "method_id": "m006",
      "summary": "获取指定道具效果的当前叠加层数。",
      "use_cases": [
        "了解某一效果被叠加的次数",
        "监控效果强度"
      ],
      "key_methods": [
        "GetCollectibleEffectNum",
        "GetCollectibleEffect"
      ]
    },
    {
      "method_id": "m007",
      "summary": "返回包含所有当前临时效果的列表，可遍历每个效果项。",
      "use_cases": [
        "遍历玩家所有临时效果进行统一处理",
        "调试输出当前效果清单"
      ],
      "key_methods": [
        "GetEffectsList"
      ]
    },
    {
      "method_id": "m008",
      "summary": "获取指定空物品类型的TemporaryEffect对象，用于查询其内部状态。",
      "use_cases": [
        "检查某空物品效果的详细属性"
      ],
      "key_methods": [
        "GetNullEffect",
        "GetNullEffectNum",
        "HasNullEffect"
      ]
    },
    {
      "method_id": "m009",
      "summary": "获取指定空物品效果的当前叠加层数。",
      "use_cases": [
        "了解空物品效果叠加次数"
      ],
      "key_methods": [
        "GetNullEffectNum",
        "GetNullEffect"
      ]
    },
    {
      "method_id": "m010",
      "summary": "获取指定饰品类型的TemporaryEffect对象，用于读取其状态。",
      "use_cases": [
        "检查饰品临时效果的详细数据"
      ],
      "key_methods": [
        "GetTrinketEffect",
        "GetTrinketEffectNum",
        "HasTrinketEffect"
      ]
    },
    {
      "method_id": "m011",
      "summary": "获取指定饰品效果的当前叠加层数。",
      "use_cases": [
        "了解饰品效果叠加的次数"
      ],
      "key_methods": [
        "GetTrinketEffectNum",
        "GetTrinketEffect"
      ]
    },
    {
      "method_id": "m012",
      "summary": "检测玩家是否拥有指定的道具效果。",
      "use_cases": [
        "条件判断是否已施加某种效果",
        "避免重复添加相同效果"
      ],
      "key_methods": [
        "HasCollectibleEffect",
        "GetCollectibleEffect",
        "AddCollectibleEffect"
      ]
    },
    {
      "method_id": "m013",
      "summary": "检测玩家是否拥有指定的空物品效果。",
      "use_cases": [
        "判断空物品是否生效"
      ],
      "key_methods": [
        "HasNullEffect",
        "GetNullEffect",
        "AddNullEffect"
      ]
    },
    {
      "method_id": "m014",
      "summary": "检测玩家是否拥有指定的饰品效果。",
      "use_cases": [
        "判断饰品效果是否已存在"
      ],
      "key_methods": [
        "HasTrinketEffect",
        "GetTrinketEffect",
        "AddTrinketEffect"
      ]
    },
    {
      "method_id": "m015",
      "summary": "移除指定道具效果，可指定移除数量，传入-1移除所有该效果实例。",
      "use_cases": [
        "减少或完全消除道具效果",
        "控制效果堆叠上限"
      ],
      "key_methods": [
        "RemoveCollectibleEffect",
        "AddCollectibleEffect",
        "HasCollectibleEffect"
      ]
    },
    {
      "method_id": "m016",
      "summary": "移除指定空物品效果，可指定数量，-1则全部移除。",
      "use_cases": [
        "撤销空物品效果"
      ],
      "key_methods": [
        "RemoveNullEffect",
        "AddNullEffect",
        "HasNullEffect"
      ]
    },
    {
      "method_id": "m017",
      "summary": "移除指定饰品效果，可指定数量，-1则全部移除。",
      "use_cases": [
        "撤销饰品临时效果"
      ],
      "key_methods": [
        "RemoveTrinketEffect",
        "AddTrinketEffect",
        "HasTrinketEffect"
      ]
    }
  ]
}
```
