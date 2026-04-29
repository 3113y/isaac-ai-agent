# DeepSeek Context

- class: RoomConfigRoom
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T14:07:10.487832

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

类名：RoomConfigRoom

原始 md 文档（该类完整文档，可能已截断）：
# Class "RoomConfigRoom"
???+ info
    You can get this class by using the following functions:

    * [RoomDescriptor.Data](RoomDescriptor.md#data)
    * [RoomDescriptor.OverrideData](RoomDescriptor.md#overridedata)

    ???+ example "Example Code"
        ```lua
        local game = Game()
        local level = game:GetLevel()
        local roomDescriptor = level:GetCurrentRoomDesc()
        local roomConfigRoom = roomDescriptor.Data
        ```

## Variables
### Difficulty {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int Difficulty {: .copyable aria-label='Variables' }
The difficulty of the room, as defined in the room editor. Typically either 5, 10, 15, or 20 for Void rooms, although mods can add rooms with any difficulty. Difficulty 0 means this room cannot show up naturally.

___
### Doors {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int Doors  {: .copyable aria-label='Variables' }
Returns a bit mask of the positions of valid door positions in this room. It is  a combination of bit flags of the DoorSlotFlag enum, which is defined as follows:

```lua
enum DoorSlotFlag {
  LEFT0 = 1 << DoorSlot.LEFT0,
  UP0 = 1 << DoorSlot.UP0,
  RIGHT0 = 1 << DoorSlot.RIGHT0,
  DOWN0 = 1 << DoorSlot.DOWN0,
  LEFT1 = 1 << DoorSlot.LEFT1,
  UP1 = 1 << DoorSlot.UP1,
  RIGHT1 = 1 << DoorSlot.RIGHT1,
  DOWN1 = 1 << DoorSlot.DOWN1,
}
```
___
### Height {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int Height  {: .copyable aria-label='Variables' }

___
### Initial·Weight {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const float InitialWeight  {: .copyable aria-label='Variables' }

___
### Mode {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .reporplus .tooltip .badge }
#### const userdata Mode  {: .copyable aria-label='Variables' }
???+ bug "Bug"
    This variable is broken and returns userdata.

___
### Name {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const string Name  {: .copyable aria-label='Variables' }

___
### Original·Variant {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### int OriginalVariant  {: .copyable aria-label='Variables' }

___
### Shape {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [RoomShape](enums/RoomShape.md) Shape  {: .copyable aria-label='Variables' }

___
### Spawn·Count {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int SpawnCount  {: .copyable aria-label='Variables' }

___
### Spawns {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [RoomConfigSpawns](CppContainer_ArrayProxy_RoomConfigSpawns.md) Spawns  {: .copyable aria-label='Variables' }

___
### Stage·ID {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int StageID  {: .copyable aria-label='Variables' }
The ID of the stage the room was designed for.

???- note "Stage IDs (corresponds to IDs in stages.xml)"

	|DLC|ID|Stage|Comment|
	|:--|:--|:--|:--|
	|[ ](#){: .alldlc .tooltip .badge }|0 |Special Rooms |  |
	|[ ](#){: .alldlc .tooltip .badge }|1 |Basement |  |
	|[ ](#){: .alldlc .tooltip .badge }|2 |Cellar |  |
	|[ ](#){: .alldlc .tooltip .badge }|3 |Burning Basement |  |
	|[ ](#){: .alldlc .tooltip .badge }|4 |Caves |  |
	|[ ](#){: .alldlc .tooltip .badge }|5 |Catacombs |  |
	|[ ](#){: .alldlc .tooltip .badge }|6 |Flooded Caves |  |
	|[ ](#){: .alldlc .tooltip .badge }|7 |Depths |  |
	|[ ](#){: .alldlc .tooltip .badge }|8 |Necropolis |  |
	|[ ](#){: .alldlc .tooltip .badge }|9 |Dank Depths |  |
	|[ ](#){: .alldlc .tooltip .badge }|10 |Womb |  |
	|[ ](#){: .alldlc .tooltip .badge }|11 |Utero |  |
	|[ ](#){: .alldlc .tooltip .badge }|12 |Scarred Womb |  |
	|[ ](#){: .alldlc .tooltip .badge }|13 |Blue Womb |  |
	|[ ](#){: .alldlc .tooltip .badge }|14 |Sheol |  |
	|[ ](#){: .alldlc .tooltip .badge }|15 |Cathedral |  |
	|[ ](#){: .alldlc .tooltip .badge }|16 |Dark Room |  |
	|[ ](#){: .alldlc .tooltip .badge }|17 |Chest |  |
	|[ ](#){: .abp .tooltip .badge }|18 |Greed Special Rooms |  |
	|[ ](#){: .abp .tooltip .badge }|19 |Greed Basement |  |
	|[ ](#){: .abp .tooltip .badge }|20 |Greed Caves |  |
	|[ ](#){: .abp .tooltip .badge }|21 |Greed Depths |  |
	|[ ](#){: .abp .tooltip .badge }|22 |Greed Womb |  |
	|[ ](#){: .abp .tooltip .badge }|23 |Greed Sheol |  |
	|[ ](#){: .alldlc .tooltip .badge }|24 |The Shop |  |
	|[ ](#){: .alldlc .tooltip .badge }|25 |Ultra Greed |  |
	|[ ](#){: .alldlc .tooltip .badge }|26 |The Void |  |
	|[ ](#){: .reporplus .tooltip .badge }|27 |Downpour |  |
	|[ ](#){: .reporplus .tooltip .badge }|28 |Dross |  |
	|[ ](#){: .reporplus .tooltip .badge }|29 |Mines |  |
	|[ ](#){: .reporplus .tooltip .badge }|30 |Ashpit |  |
	|[ ](#){: .reporplus .tooltip .badge }|31 |Mausoleum |  |
	|[ ](#){: .reporplus .tooltip .badge }|32 |Gehenna |  |
	|[ ](#){: .reporplus .tooltip .badge }|33 |Corpse |  |
	|[ ](#){: .reporplus .tooltip .badge }|35 |Home |The Stage ID of 34 does not exist. |
	|[ ](#){: .reporplus .tooltip .badge }|36 |Backwards |These rooms are used during the Ascent. |

___
### Subtype {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int Subtype  {: .copyable aria-label='Variables' }

___
### Type {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [RoomType](enums/RoomType.md) Type  {: .copyable aria-label='Variables' }

___
### Variant {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int Variant  {: .copyable aria-label='Variables' }

___
### Weight {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const float Weight  {: .copyable aria-label='Variables' }

___
### Width {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int Width  {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "Difficulty",
    "signature": "const int Difficulty {: .copyable aria-label='Variables' }",
    "description": "The difficulty of the room, as defined in the room editor. Typically either 5, 10, 15, or 20 for Void rooms, although mods can add rooms with any difficulty. Difficulty 0 means this room cannot show up naturally."
  },
  {
    "method_id": "m002",
    "name": "Doors",
    "signature": "const int Doors  {: .copyable aria-label='Variables' }",
    "description": "Returns a bit mask of the positions of valid door positions in this room. It is  a combination of bit flags of the DoorSlotFlag enum, which is defined as follows:"
  },
  {
    "method_id": "m003",
    "name": "Height",
    "signature": "const int Height  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "InitialWeight",
    "signature": "const float InitialWeight  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "Mode",
    "signature": "const userdata Mode  {: .copyable aria-label='Variables' }",
    "description": "???+ bug \"Bug\""
  },
  {
    "method_id": "m006",
    "name": "Name",
    "signature": "const string Name  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "OriginalVariant",
    "signature": "int OriginalVariant  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "Shape",
    "signature": "const [RoomShape](enums/RoomShape.md) Shape  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "SpawnCount",
    "signature": "const int SpawnCount  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "Spawns",
    "signature": "const [RoomConfigSpawns](CppContainer_ArrayProxy_RoomConfigSpawns.md) Spawns  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "StageID",
    "signature": "const int StageID  {: .copyable aria-label='Variables' }",
    "description": "The ID of the stage the room was designed for."
  },
  {
    "method_id": "m012",
    "name": "Subtype",
    "signature": "const int Subtype  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "Type",
    "signature": "const [RoomType](enums/RoomType.md) Type  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "Variant",
    "signature": "const int Variant  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "Weight",
    "signature": "const float Weight  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m016",
    "name": "Width",
    "signature": "const int Width  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "RoomConfigRoom provides read-only access to a room's configuration as defined in the room editor, including dimensions, door placements, spawn points, type identifiers, and weighting for procedural generation.",
    "use_cases": [
      "Reading room configuration data for custom room generation",
      "Determining valid door positions and room connectivity",
      "Accessing enemy spawn points and their properties",
      "Filtering rooms by stage, type, variant, or difficulty",
      "Debugging room properties during level generation"
    ],
    "key_methods": [
      "Type",
      "Variant",
      "Subtype",
      "Doors",
      "Spawns"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "Returns the room's difficulty level, typically 5, 10, 15, or 20 for special rooms; 0 means the room cannot appear naturally.",
      "use_cases": [
        "Filtering rooms by difficulty in custom generation",
        "Assigning difficulty-based rewards",
        "Ensuring only challenging rooms appear in end-game floors"
      ],
      "key_methods": [
        "Difficulty",
        "Weight",
        "StageID",
        "Type"
      ]
    },
    {
      "method_id": "m002",
      "summary": "Returns a bitmask of valid door positions using the DoorSlotFlag enum, indicating which walls can have doors.",
      "use_cases": [
        "Determining which sides of a room can connect to adjacent rooms",
        "Preventing invalid door placements in modded rooms",
        "Custom room shape and connectivity detection"
      ],
      "key_methods": [
        "Doors",
        "Shape",
        "Width",
        "Height"
      ]
    },
    {
      "method_id": "
```
