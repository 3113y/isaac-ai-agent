# DeepSeek Context

- class: RoomDescriptor
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T14:09:51.466438

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

类名：RoomDescriptor

原始 md 文档（该类完整文档，可能已截断）：
# Class "RoomDescriptor"

???+ info
    You can get this class by using the following functions:

    * [Level:GetCurrentRoomDesc()](Level.md#getcurrentroomdesc)
    * [Level:GetLastRoomDesc()](Level.md#getlastroomdesc)
    * [Level:GetRoomByIdx()](Level.md#getroombyidx)

    ???+ example "Example Code"
        ```lua
        local level = Game():GetLevel()
        local roomDescriptor = level:GetCurrentRoomDesc()
        ```

## Variables
### Allowed·Doors {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### DoorSet AllowedDoors  {: .copyable aria-label='Variables' }
Contains data swapped just on load (in cases like minibosses, or other such events)

???+ bug "Bug"
    This variable contains userdata and is therefore not useable.
___
### Award·Seed {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AwardSeed  {: .copyable aria-label='Variables' }
used to spawn clear awards (normal, miniboss, boss rooms) and initialize shop items (shop, devil rooms)
___
### Challenge·Done {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean ChallengeDone  {: .copyable aria-label='Variables' }

___
### Clear {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean Clear  {: .copyable aria-label='Variables' }

___
### Clear·Count {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ClearCount  {: .copyable aria-label='Variables' }
room is clear, don't spawn enemies when visiting
___
### Data {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [RoomConfigRoom](RoomConfig_Room.md) Data  {: .copyable aria-label='Variables' }

___
### Decoration·Seed {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int DecorationSeed  {: .copyable aria-label='Variables' }
used for cosmetic stuff like backdrops, room decorations, shopkeeper skins
___
### Delirium·Distance {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int DeliriumDistance  {: .copyable aria-label='Variables' }
Helper for The Void stage, holds the distance to the Delirium boss in room nr.
___
### Display·Flags {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int DisplayFlags  {: .copyable aria-label='Variables' }

Indicates what is visible on the minimap.
**Display Flags (bitwise):**
```lua
1 << -1 -- Invisible
1 << 0 -- Visible
1 << 1 -- Room Shadow
1 << 2 -- Show Icon
```

???- example "Examples"
    The flags are hard to interpret, but here are some examples:

    **000** = invisible, this is how most rooms start

    **101** = standard room visibility, this includes rooms that are adjacent and you haven't actively visited. This will usually show icons.

    **011** = secret room, locked rooms, sac rooms pre-entry*

    **111** = 011 rooms after entry, but also the rooms directly adjacent to them* (applied after entry)

    \* If you have Spelunker Hat, bit 1 is completely unused. All special rooms will have the normal behavior of either 000 or 101. This is unique to Spelunker Hat; mapping items follow the normal rules.

???+ quote "Quote from User 'Budj'"
    From this my best guess is that bits 1 and 2 are special rendering (display) flags that may have more meaning down below.

    The important bit for using them is minding that they're used differently mostly for special rooms.

    As far as I've seen, 001 is completely unused.
    010, 100, and 110 may be used for compass or blue map, I don't remember. I think they use 100.
___
### Flags {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [RoomDescriptor](enums/RoomDescriptor.md) Flags  {: .copyable aria-label='Variables' }
The RoomDescriptor flags for the room.
___
### Grid·Index {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int GridIndex  {: .copyable aria-label='Variables' }

Describes the index of the room on the level grid (13 by 13 cells). The index is the cell number on the grid, when counting them row by row from left to right.

- For a 1x1 room, this is equal to the 1x1 grid index of the room.
- For a room bigger than a 1x1 room, this is equal to the top left 1x1 quadrant.
- For `RoomType.ROOMSHAPE_LTL` rooms (i.e. rooms that look like a "J"), this is equal to the 1x1 quadrant where the gap in the room is. In other words, it is a 1x1 quadrant that is not actually contained within the room.
- Note that **this value is different** than the value returned by `Level:GetCurrentRoomIndex()`. (That function returns the 1x1 quadrant that the room was entered in.)
- Data structures that store data per room should use `ListIndex` as a key instead of `GridIndex`, since the former is unique across different dimensions.

???- note "Notes"
    ![Room Grid indices](images/infographics/RoomGridIndices.png)

???- example "Get dimension example code"
    A level can have multiple dimensions, which act as separate and independent level grids. Because of this, a room in dimension 1 can share the same grid index as a different room in dimension 2. Repentogon provides a GetDimension method, but if you don’t have access to it, you can use the following function to determine the dimension of a given room descriptor.

    ```lua
    -- requirements: a room that actually exists on the map, or one of the game's special rooms that exist outside the map
    local function getDimension(roomDesc)
      -- 0: main dimension
      -- 1: secondary dimension, used by downpour mirror dimension and mines escape sequence
      -- 2: death certificate dimension
      for i = 0, 2 do
        if GetPtrHash(roomDesc) == GetPtrHash(Game():GetLevel():GetRoomByIdx(roomDesc.SafeGridIndex, i)) then
          return i
        end
      end
      return -1
    end

    getDimension(Game():GetLevel():GetCurrentRoomDesc()) -- returns 0, 1, or 2 depending on where you're at
    getDimension(Game():GetLevel():GetRoomByIdx(GridRooms.ROOM_DEVIL_IDX)) -- special rooms outside the map return 0
    ```
___
### Has·Water {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean HasWater  {: .copyable aria-label='Variables' }

___
### List·Index {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ListIndex  {: .copyable aria-label='Variables' }

The index for this room corresponding to the `Level.GetRooms().Get()` method. In other words, this is equal to the order that the room was created by the floor generation algorithm.

Use this as an index for data structures that store data per room, since it is unique across different dimensions.

___
### No·Reward {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean NoReward  {: .copyable aria-label='Variables' }

___
### Override·Data {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [RoomConfigRoom](RoomConfig_Room.md) OverrideData  {: .copyable aria-label='Variables' }
The room variant is in Data. Because Room::Init uses a mix of data, one from level layout and one from replacement data like minibosses, we need to hold the new room data somewhere.
___
### Pits·Count {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int PitsCount  {: .copyable aria-label='Variables' }

___
### Poop·Count {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int PoopCount  {: .copyable aria-label='Variables' }

___
### Pressure·Plates·Triggered {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean PressurePlatesTriggered  {: .copyable aria-label='Variables' }

___
### Sacrifice·Done {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean SacrificeDone  {: .copyable aria-label='Variables' }

___
### Safe·Grid·Index {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int SafeGridIndex  {: .copyable aria-label='Variables' }

- For a 1x1 room, this is equal to the 1x1 grid index of the room.
- For a room bigger than a 1x1 room, this is equal to the top left 1x1 quadrant.
- For `RoomType.ROOMSHAPE_LTL` rooms (i.e. rooms that look like a "J"), this is equal to the top right 1x1 quadrant.
- Note that **this value is different** than the value returned by `Level:GetCurrentRoomIndex()`. (That function returns the 1x1 quadrant that the room was entered in.)
- Data structures that store data per room should use `ListIndex` as a key instead of `SafeGridIndex`, since the former is unique across different dimensions.

???- note "Notes"
    ![Room Grid indices](images/infographics/RoomGridIndices.png)
___
### Shop·Item·Discount·Idx {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ShopItemDiscountIdx  {: .copyable aria-label='Variables' }
- The index that denotes which shop item(s) will be discounted.
- Can be a value from -1 to 7.
- All items in the room with this ShopItemId will be affected by the discount.
    - This is noticeable when there are more than 8 shop items in a room.
- A value of -1 means there is no discounted item.
- This value is unaffected by Steam Sale.
- Defaults to -1 in non-shop rooms.
- Can be modified by accessing the writable version of the RoomDescriptor like this:

```lua
local level = Game():GetLevel()
local room = level:GetCurrentRoom()

-- this returns a writable RoomDescriptor for the current Room.
local writableRoomDesc = level:GetRoomByIdx(level:GetCurrentRoomIndex())

-- Sets the current Room's ShopItemDiscountIdx to 0.
-- All items with ShopItemId 0 will be discounted.
writableRoomDesc.ShopItemDiscountIdx = 0

-- update the Room using Update() to have the change take effect.
room:Update()
```

___
### Shop·Item·Idx {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ShopItemIdx  {: .copyable aria-label='Variables' }
- The ShopItemId value of the next shop item to add to the room.
    - If this is set to 1 in a Room and another shop item is created, the new item will have a ShopItemId of 1, and the Room's ShopItemIdx will then be 2.
- Can be used as the total number of items in the shop, up to 7 items.
- Can be a value between 0 and 7.
- For every 8 items in a shop, this value resets itself to 0.
    - For example, if a custom shop has 9 items, the 1st and 9th items will share the same ShopItemId of 0, and the RoomDescriptor ShopItemIdx value will be 1.
- Defaults to -1 in non-shop rooms.
- Can be modified by accessing the writable version of the RoomDescriptor like this:

```lua
local level = Game():GetLevel()
local room = level:GetCurrentRoom()

-- this returns a writable RoomDescriptor for the current Room.
local writableRoomDesc = level:GetRoomByIdx(level:GetCurrentRoomIndex())

-- Sets the current Room's ShopItemIdx to 0.
writableRoomDesc.ShopItemIdx = 0

-- update the Room using Update() to have the change take effect.
room:Update()
```

???- note "Notes"
    - In the image below, each item's ShopItemId is written underneath it.
    - Notice how all items that share a ShopItemId have the same PickupVariant, but aren't identical.
    - ShopItemDiscountIdx is 2, so all shop items with a ShopItemId of 2 are on sale.
    - After all items are created, the ShopItemIdx for this room is 0.
    ![ShopItemIdx Example](images/shopItemIdxDiagram.png)
___
### Spawn·Seed {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int SpawnSeed  {: .copyable aria-label='Variables' }
used to spawn entities at room load and initialize enemy drop seeds
___
### Surprise·Miniboss {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean SurpriseMiniboss  {: .copyable aria-label='Variables' }
___
### Visited·Count {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int VisitedCount  {: .copyable aria-label='Variables' }
how often the room has been visited
___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "AllowedDoors",
    "signature": "DoorSet AllowedDoors  {: .copyable aria-label='Variables' }",
    "description": "Contains data swapped just on load (in cases like minibosses, or other such events)"
  },
  {
    "method_id": "m002",
    "name": "AwardSeed",
    "signature": "int AwardSeed  {: .copyable aria-label='Variables' }",
    "description": "used to spawn clear awards (normal, miniboss, boss rooms) and initialize shop items (shop, devil rooms)"
  },
  {
    "method_id": "m003",
    "name": "ChallengeDone",
    "signature": "boolean ChallengeDone  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "Clear",
    "signature": "boolean Clear  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "ClearCount",
    "signature": "int ClearCount  {: .copyable aria-label='Variables' }",
    "description": "room is clear, don't spawn enemies when visiting"
  },
  {
    "method_id": "m006",
    "name": "Data",
    "signature": "[RoomConfigRoom](RoomConfig_Room.md) Data  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "DecorationSeed",
    "signature": "int DecorationSeed  {: .copyable aria-label='Variables' }",
    "description": "used for cosmetic stuff like backdrops, room decorations, shopkeeper skins"
  },
  {
    "method_id": "m008",
    "name": "DeliriumDistance",
    "signature": "int DeliriumDistance  {: .copyable aria-label='Variables' }",
    "description": "Helper for The Void stage, holds the distance to the Delirium boss in room nr."
  },
  {
    "method_id": "m009",
    "name": "DisplayFlags",
    "signature": "int DisplayFlags  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "Flags",
    "signature": "[RoomDescriptor](enums/RoomDescriptor.md) Flags  {: .copyable aria-label='Variables' }",
    "description": "The RoomDescriptor flags for the room."
  },
  {
    "method_id": "m011",
    "name": "GridIndex",
    "signature": "int GridIndex  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "HasWater",
    "signature": "boolean HasWater  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "ListIndex",
    "signature": "int ListIndex  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "NoReward",
    "signature": "boolean NoReward  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "OverrideData",
    "signature": "[RoomConfigRoom](RoomConfig_Room.md) OverrideData  {: .copyable aria-label='Variables' }",
    "description": "The room variant is in Data. Because Room::Init uses a mix of data, one from level layout and one from replacement data like minibosses, we need to hold the new room data somewhere."
  },
  {
    "method_id": "m016",
    "name": "PitsCount",
    "signature": "int PitsCount  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m017",
    "name": "PoopCount",
    "signature": "int PoopCount  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m018",
    "name": "PressurePlatesTriggered",
    "signature": "boolean PressurePlatesTriggered  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m019",
    "name": "SacrificeDone",
    "signature": "boolean SacrificeDone  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m020",
    "name": "SafeGridIndex",
    "signature": "int SafeGridIndex  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m021",
    "name": "ShopItemDiscountIdx",
    "signature": "int ShopItemDiscountIdx  {: .copyable aria-label='Variables' }",
    "description": "- The index that denotes which shop item(s) will be discounted."
  },
  {
    "method_id": "m022",
    "name": "ShopItemIdx",
    "signature": "int ShopItemIdx  {: .copyable aria-label='Variables' }",
    "description": "- The ShopItemId value of the next shop item to add to the room."
  },
  {
    "method_id": "m023",
    "name": "SpawnSeed",
    "signature": "int SpawnSeed  {: .copyable aria-label='Variables' }",
    "description": "used to spawn entities at room load and initialize enemy drop seeds"
  },
  {
    "method_id": "m024",
    "name": "SurpriseMiniboss",
    "signature": "boolean SurpriseMiniboss  {: .copyable aria-label='Variables' }",
    "description": "___"
  },
  {
    "method_id": "m025",
    "name": "VisitedCount",
    "signature": "int VisitedCount  {: .copyable aria-label='Variables' }",
    "description": "how often the room has been visited"
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "RoomDescriptor 存储一个房间的元数据和状态信息，包括房间类型、清理状态、生成种子、网格索引和商店相关数据等。",
    "use_cases": [
      "获取房间配置数据",
      "检查房间是否清理或受挑战",
      "获取或设置商店物品折扣和索引",
      "获取房间网格索引用于寻路",
      "判断房间特殊状态如是否有水、陷阱等"
    ],
    "key_methods": [
      "Data",
      "Flags",
      "GridIndex",
      "Clear",
      "ShopItemDiscountIdx"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "存储房间允许的门数据，在加载时使用（如小Boss事件），但包含用户数据无法直接使用。",
      "use_cases": [],
      "key_methods": [
        "AllowedDoors"
      ]
    },
    {
      "method_id": "m002",
      "summary": "用于生成通关奖励（普通、小Boss、Boss房）和初始化商店物品（商店、恶魔房）的种子。",
      "use_cases": [
        "生成房间奖励",
        "初始化商店物品"
      ],
      "key_methods": [
        "AwardSeed",
        "SpawnSeed"
      ]
    },
    {
      "method_id": "m003",
      "summary": "标记房间是否已完成挑战。",
      "use_cases": [
        "检查挑战是否完成"
      ],
      "key_methods": [
        "ChallengeDone",
        "Clear"
      ]
    },
    {
      "method_id": "m004",
      "summary": "标记房间是否已清理。",
      "use_cases": [
        "判断房间是否清空敌人"
      ],
      "key_methods": [
        "Clear",
        "ClearCount"
      ]
    },
    {
      "method_id": "m005",
      "summary": "房间被清理的次数，用于判断是否已经清除敌人而不再次生成。",
      "use_cases": [
        "防止重新访问时生成敌人"
      ],
      "key_methods": [
        "ClearCount",
        "Clear"
      ]
    },
    {
      "method_id": "m006",
      "summary": "返回房间的配置数据（RoomConfigRoom）。",
      "use_cases": [
        "获取房间类型和布局信息"
      ],
      "key_methods": [
        "Data",
        "OverrideData"
      ]
    },
    {
      "method_id": "m007",
      "summary": "用于装饰元素的种子，如背景、房间装饰、店主皮肤等。",
      "use_cases": [
        "生成随机装饰"
      ],
      "key_methods": [
        "DecorationSeed"
      ]
    },
    {
      "method_id": "m008",
      "summary": "在虚空层中记录当前房间距离百变怪Boss的步数。",
      "use_cases": [
        "虚空层导航提示"
      ],
      "key_methods": [
        "DeliriumDistance"
      ]
    },
    {
      "method_id": "m009",
      "summary": "控制小地图上该房间的可见性和图标显示，使用位标志。",
      "use_cases": [
        "设置或读取房间在小地图上的展示状态"
      ],
      "key_methods": [
        "DisplayFlags"
      ]
    },
    {
      "method_id": "m010",
      "summary": "房间描述符的标志位，表示房间的全局属性。",
      "use_cases": [
        "判断房间是否为特殊类型"
      ],
      "key_methods": [
        "Flags",
        "Data"
      ]
    },
    {
      "method_id": "m011",
      "summary": "房间在 13x13 网格中的索引，参照左上象限，对于特殊形状可能指向空洞位置。",
      "use_cases": [
        "定位房间在关卡中的位置"
      ],
      "key_methods": [
        "GridIndex",
        "SafeGridIndex",
        "ListIndex"
      ]
    },
    {
      "method_id": "m012",
      "summary": "表示房间内是否有水。",
      "use_cases": [
        "判定水坑等环境要素"
      ],
      "key_methods": [
        "HasWater"
      ]
    },
    {
      "method_id": "m013",
      "summary": "房间在生成顺序中的唯一索引，适合用作数据结构的键值。",
      "use_cases": [
        "作为房间数据存储的标识"
      ],
      "key_methods": [
        "ListIndex",
        "GridIndex"
      ]
    },
    {
      "method_id": "m014",
      "summary": "标记房间是否不提供通关奖励。",
      "use_cases": [
        "禁用特定房间的奖励"
      ],
      "key_methods": [
        "NoReward",
        "AwardSeed"
      ]
    },
    {
      "method_id": "m015",
      "summary": "保存覆盖的房间数据，用于小Boss替换等场景。",
      "use_cases": [
        "实现房间类型动态替换"
      ],
      "key_methods": [
        "OverrideData",
        "Data"
      ]
    },
    {
      "method_id": "m016",
      "summary": "房间内坑的数量。",
      "use_cases": [
        "了解房间危险程度"
      ],
      "key_methods": [
        "PitsCount"
      ]
    },
    {
      "method_id": "m017",
      "summary": "房间内粪堆的数量。",
      "use_cases": [
        "计算特定实体数量"
      ],
      "key_methods": [
        "PoopCount"
      ]
    },
    {
      "method_id": "m018",
      "summary": "表示压力板是否已被触发。",
      "use_cases": [
        "判断机关状态"
      ],
      "key_methods": [
        "PressurePlatesTriggered"
      ]
    },
    {
      "method_id": "m019",
      "summary": "标记献祭是否完成。",
      "use_cases": [
        "控制献祭事件进度"
      ],
      "key_methods": [
        "SacrificeDone",
        "ChallengeDone"
      ]
    },
    {
      "method_id": "m020",
      "summary": "安全的网格索引，总是返回房间实际所占的左上象限，即使形状特殊也返回安全坐标。",
      "use_cases": [
        "确保获取有效的房间坐标"
      ],
      "key_methods": [
        "SafeGridIndex",
        "GridIndex"
      ]
    },
    {
      "method_id": "m021",
      "summary": "指定哪个ShopItemId的商品享受折扣，-1表示无折扣。",
      "use_cases": [
        "实现商店打折逻辑",
        "修改打折物品"
      ],
      "key_methods": [
        "ShopItemDiscountIdx",
        "ShopItemIdx"
      ]
    },
    {
      "method_id": "m022",
      "summary": "下一个要添加的商店物品的ShopItemId，或表示当前总物品数模8的值。",
      "use_cases": [
        "管理商店物品生成顺序",
        "确定物品ID重复周期"
      ],
      "key_methods": [
        "ShopItemIdx",
        "ShopItemDiscountIdx"
      ]
    },
    {
      "method_id": "m023",
      "summary": "用于生成房间内实体和敌人掉落种子的种子值。",
      "use_cases": [
        "控制实体生成和掉落"
      ],
      "key_methods": [
        "SpawnSeed",
        "AwardSeed"
      ]
    },
    {
      "method_id": "m024",
      "summary": "标记该房间是否有一个突袭小Boss。",
      "use_cases": [
        "判断触发的战斗类型"
      ],
      "key_methods": [
        "SurpriseMiniboss"
      ]
    },
    {
      "method_id": "m025",
      "summary": "记录该房间被访问过的次数。",
      "use_cases": [
        "追踪重复访问情况"
      ],
      "key_methods": [
        "VisitedCount"
      ]
    }
  ]
}
```
