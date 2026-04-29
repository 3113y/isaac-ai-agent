# DeepSeek Context

- class: GridEntityDoor
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:32:56.776315

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

类名：GridEntityDoor

原始 md 文档（该类完整文档，可能已截断）：
# Class "GridEntityDoor"

???+ info
    You can get this class by using the following function:

    * [GridEntity.ToDoor()](GridEntity.md#todoor)
    * [Room.GetDoor()](Room.md#getdoor)

    ???+ example "Example Code"
        `Game():GetRoom():GetGridEntity(25):ToDoor()`

## Class Diagram
--8<-- "docs/snippets/GridEntityClassDiagram.md"
## Functions
### Bar () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void Bar ( ) {: .copyable aria-label='Functions' }

___
### Can·Blow·Open () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean CanBlowOpen ( ) {: .copyable aria-label='Functions' }

___
### Close () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void Close ( boolean Force ) {: .copyable aria-label='Functions' }

___
### Get·Sprite·Offset () {: aria-label='Functions' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [Vector](Vector.md) GetSpriteOffset ( ) {: .copyable aria-label='Functions' }

___
### Is·Busted () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsBusted ( ) {: .copyable aria-label='Functions' }

___
### Is·Key·Familiar·Target () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsKeyFamiliarTarget ( ) {: .copyable aria-label='Functions' }

___
### Is·Locked () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsLocked ( ) {: .copyable aria-label='Functions' }

___
### Is·Open () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsOpen ( ) {: .copyable aria-label='Functions' }

___
### Is·Room·Type () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsRoomType ( [RoomType](enums/RoomType.md) Type ) {: .copyable aria-label='Functions' }

___
### Is·Target·Room·Arcade () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsTargetRoomArcade ( ) {: .copyable aria-label='Functions' }

___
### Open () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void Open ( ) {: .copyable aria-label='Functions' }

___
### Set·Locked () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetLocked ( boolean Locked ) {: .copyable aria-label='Functions' }

___
### Set·Room·Types () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetRoomTypes ( [RoomType](enums/RoomType.md) CurrentRoomType, [RoomType](enums/RoomType.md) TargetRoomType ) {: .copyable aria-label='Functions' }

___
### Spawn·Dust () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SpawnDust ( ) {: .copyable aria-label='Functions' }

___
### Try·Blow·Open () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean TryBlowOpen ( boolean FromExplosion, [Entity](Entity.md) source ) {: .copyable aria-label='Functions' }
try to open the door by explosive force, true for success
___
### Try·Unlock () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean TryUnlock ([EntityPlayer](EntityPlayer.md) player, boolean Force ) {: .copyable aria-label='Functions' }
try to unlock the door using a key, true for success
___
## Variables
### Busted {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean Busted  {: .copyable aria-label='Variables' }

___
### Close·Animation {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string CloseAnimation  {: .copyable aria-label='Variables' }

___
### Current·Room·Type {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [RoomType](enums/RoomType.md) CurrentRoomType  {: .copyable aria-label='Variables' }

___
### Direction {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Direction](enums/Direction.md) Direction {: .copyable aria-label='Variables' }

___
### Extra·Sprite {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Sprite](Sprite.md) ExtraSprite  {: .copyable aria-label='Variables' }
Additional sprite used for the door. Examples for extra sprites are: bars, chains, wooden boards, etc.
___
### Extra·Visible {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean ExtraVisible  {: .copyable aria-label='Variables' }
Toggles the visibility of the extra sprite. Examples for extra sprites are: bars, chains, wooden boards, etc.
___
### Locked·Animation {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string LockedAnimation  {: .copyable aria-label='Variables' }

___
### Open·Animation {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string OpenAnimation  {: .copyable aria-label='Variables' }

___
### Open·Locked·Animation {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string OpenLockedAnimation  {: .copyable aria-label='Variables' }

___
### Previous·State {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int PreviousState  {: .copyable aria-label='Variables' }
???+ bug "Bug"
    This variable is broken and returns userdata.

___
### Previous·Variant {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int PreviousVariant  {: .copyable aria-label='Variables' }
???+ bug "Bug"
    This variable is broken and returns userdata.

___
### Slot {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [DoorSlot](enums/DoorSlot.md) Slot  {: .copyable aria-label='Variables' }

___
### Target·Room·Index {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int TargetRoomIndex  {: .copyable aria-label='Variables' }
Note: this value only affects the room transition animation and does not actually change the target room.

___
### Target·Room·Type {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [RoomType](enums/RoomType.md) TargetRoomType  {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "Bar",
    "signature": "void Bar ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "CanBlowOpen",
    "signature": "boolean CanBlowOpen ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "Close",
    "signature": "void Close ( boolean Force ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "GetSpriteOffset",
    "signature": "const [Vector](Vector.md) GetSpriteOffset ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "IsBusted",
    "signature": "boolean IsBusted ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "IsKeyFamiliarTarget",
    "signature": "boolean IsKeyFamiliarTarget ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "IsLocked",
    "signature": "boolean IsLocked ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "IsOpen",
    "signature": "boolean IsOpen ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "IsRoomType",
    "signature": "boolean IsRoomType ( [RoomType](enums/RoomType.md) Type ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "IsTargetRoomArcade",
    "signature": "boolean IsTargetRoomArcade ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "Open",
    "signature": "void Open ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "SetLocked",
    "signature": "void SetLocked ( boolean Locked ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "SetRoomTypes",
    "signature": "void SetRoomTypes ( [RoomType](enums/RoomType.md) CurrentRoomType, [RoomType](enums/RoomType.md) TargetRoomType ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "SpawnDust",
    "signature": "void SpawnDust ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "TryBlowOpen",
    "signature": "boolean TryBlowOpen ( boolean FromExplosion, [Entity](Entity.md) source ) {: .copyable aria-label='Functions' }",
    "description": "try to open the door by explosive force, true for success"
  },
  {
    "method_id": "m016",
    "name": "TryUnlock",
    "signature": "boolean TryUnlock ([EntityPlayer](EntityPlayer.md) player, boolean Force ) {: .copyable aria-label='Functions' }",
    "description": "try to unlock the door using a key, true for success"
  },
  {
    "method_id": "m017",
    "name": "Busted",
    "signature": "boolean Busted  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m018",
    "name": "CloseAnimation",
    "signature": "string CloseAnimation  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m019",
    "name": "CurrentRoomType",
    "signature": "[RoomType](enums/RoomType.md) CurrentRoomType  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m020",
    "name": "Direction",
    "signature": "[Direction](enums/Direction.md) Direction {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m021",
    "name": "ExtraSprite",
    "signature": "[Sprite](Sprite.md) ExtraSprite  {: .copyable aria-label='Variables' }",
    "description": "Additional sprite used for the door. Examples for extra sprites are: bars, chains, wooden boards, etc."
  },
  {
    "method_id": "m022",
    "name": "ExtraVisible",
    "signature": "boolean ExtraVisible  {: .copyable aria-label='Variables' }",
    "description": "Toggles the visibility of the extra sprite. Examples for extra sprites are: bars, chains, wooden boards, etc."
  },
  {
    "method_id": "m023",
    "name": "LockedAnimation",
    "signature": "string LockedAnimation  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m024",
    "name": "OpenAnimation",
    "signature": "string OpenAnimation  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m025",
    "name": "OpenLockedAnimation",
    "signature": "string OpenLockedAnimation  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m026",
    "name": "PreviousState",
    "signature": "int PreviousState  {: .copyable aria-label='Variables' }",
    "description": "???+ bug \"Bug\""
  },
  {
    "method_id": "m027",
    "name": "PreviousVariant",
    "signature": "int PreviousVariant  {: .copyable aria-label='Variables' }",
    "description": "???+ bug \"Bug\""
  },
  {
    "method_id": "m028",
    "name": "Slot",
    "signature": "[DoorSlot](enums/DoorSlot.md) Slot  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m029",
    "name": "TargetRoomIndex",
    "signature": "int TargetRoomIndex  {: .copyable aria-label='Variables' }",
    "description": "Note: this value only affects the room transition animation and does not actually change the target room."
  },
  {
    "method_id": "m030",
    "name": "TargetRoomType",
    "signature": "[RoomType](enums/RoomType.md) TargetRoomType  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "表示游戏中的门网格实体，负责管理门的开闭、锁定、动画、目标房间类型以及与钥匙、炸弹的交互。",
    "use_cases": [
      "管理门的打开、关闭与锁定状态",
      "探测门是否通向特定房间类型（如街机厅）",
      "模拟玩家使用钥匙或炸弹开门",
      "自定义门的外观、动画和额外装饰",
      "获取门的朝向和插槽信息"
    ],
    "key_methods": [
      "Open",
      "Close",
      "TryUnlock",
      "TryBlowOpen",
      "SetLocked"
    ]
  },
  "method_enhancements": [
    {
      "method_id
```
