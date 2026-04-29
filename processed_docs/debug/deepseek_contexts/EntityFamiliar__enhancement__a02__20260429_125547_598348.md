# DeepSeek Context

- class: EntityFamiliar
- stage: enhancement
- attempt: 2
- model: deepseek-v4-pro
- max_tokens: 3400
- temperature: 0
- timestamp: 2026-04-29T12:55:47.598384

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
压缩输出：summary 尽量控制在 60 字内，use_cases 不超过 2 项，key_methods 不超过 3 项。

类名：EntityFamiliar

原始 md 文档（该类完整文档，可能已截断）：
# Class "EntityFamiliar"

???+ info
    You can get this class by using the following function:

    * [Entity.ToFamiliar()](Entity.md#tofamiliar)
    * [EntityPlayer.AddItemWisp()](EntityPlayer.md#additemwisp)
    * [EntityPlayer.AddMinisaac()](EntityPlayer.md#addminisaac)
    * [EntityPlayer.AddSwarmFlyOrbital()](EntityPlayer.md#addswarmflyorbital)
    * [EntityPlayer.AddWisp()](EntityPlayer.md#addwisp)
    * [EntityPlayer.ThrowFriendlyDip()](EntityPlayer.md#throwfriendlydip)

    ???+ example "Example Code"
        `local familiarEntity = Isaac.GetPlayer():AddMinisaac(Vector(0,0))`

## Class Diagram
--8<-- "docs/snippets/EntityClassDiagram.md"
## Functions
### Add·Coins () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddCoins ( int Value ) {: .copyable aria-label='Functions' }

___
### Add·Hearts () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddHearts ( int Hearts ) {: .copyable aria-label='Functions' }

___
### Add·Keys () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddKeys ( int Keys ) {: .copyable aria-label='Functions' }

___
### Add·To·Delayed () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddToDelayed ( ) {: .copyable aria-label='Functions' }
Adds to delayed. This doesn't remove other flags!
___
### Add·To·Followers () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddToFollowers ( ) {: .copyable aria-label='Functions' }
Adds to followers. This doesn't remove other flags!
___
### Add·To·Orbit () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddToOrbit ( int Layer ) {: .copyable aria-label='Functions' }
Adds to orbitals. This doesn't remove other flags!
___
### Fire·Projectile () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### [EntityTear](EntityTear.md) FireProjectile ( [Vector](Vector.md) Dir ) {: .copyable aria-label='Functions' }

Shoots a projectile from the center of the familiar in the direction you defined.
If used on a familiar that shoots multiple projectiles (example: harlequin baby), this function will only return the left most projectile based on the direction. If used on familiars with special tears (example: Lil Brimstone,...), this will just shoot a regular tear.
This function will not play the shoot animation of the familiar.
___
### Follow·Parent () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void FollowParent ( ) {: .copyable aria-label='Functions' }

___
### Follow·Position () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void FollowPosition ( [Vector](Vector.md) Pos ) {: .copyable aria-label='Functions' }

___
### Get·Orbit·Distance () {: aria-label='Functions' }
[ ](#){: .static .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### static [Vector](Vector.md) GetOrbitDistance ( int Layer ) {: .copyable aria-label='Functions' }

___
### Get·Orbit·Position () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) GetOrbitPosition ( [Vector](Vector.md) Pos ) {: .copyable aria-label='Functions' }

Returns the position of an orbiting familiar relative to the player's position. Returns `:::lua Vector(0,0) if its a normal familiar.`
The "pos" argument is used as an offset.
___
### Move·Delayed () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void MoveDelayed ( int NumFrames ) {: .copyable aria-label='Functions' }

___
### Move·Diagonally () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void MoveDiagonally ( float Speed ) {: .copyable aria-label='Functions' }

___
### Pick·Enemy·Target () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void PickEnemyTarget ( float MaxDistance, int FrameInterval = 13, int Flags = 0, [Vector](Vector.md) ConeDir = Vector.Zero, float ConeAngle = 15 ) {: .copyable aria-label='Functions' }
**Flags**: A combination of the following flags (none of these are set by default)

    * 1: Allow switching to a better target even if we already have one
    * 2: Don't prioritize enemies that are close to our owner
    * 4: Prioritize enemies with higher HP
    * 8: Prioritize enemies with lower HP
    * 16: Give lower priority to our current target (this makes us more likely to switch between targets)

**ConeDir**: If ~= Vector.Zero, searches for targets in a cone pointing in this direction

**ConeAngle**: If ConeDir ~= Vector.Zero, sets the half angle of the search cone in degrees (45 results in a search angle of 90 degrees)
___
### Play·Charge·Anim () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void PlayChargeAnim ( [Direction](enums/Direction.md) Dir ) {: .copyable aria-label='Functions' }

___
### Play·Float·Anim () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void PlayFloatAnim ( [Direction](enums/Direction.md) Dir ) {: .copyable aria-label='Functions' }

___
### Play·Shoot·Anim () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void PlayShootAnim ( [Direction](enums/Direction.md) Dir ) {: .copyable aria-label='Functions' }

___
### Recalculate·Orbit·Offset () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### int RecalculateOrbitOffset ( int Layer, boolean Add ) {: .copyable aria-label='Functions' }
Returns the number of familiars in that layer.
___
### Remove·From·Delayed () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void RemoveFromDelayed ( ) {: .copyable aria-label='Functions' }

___
### Remove·From·Followers () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void RemoveFromFollowers ( ) {: .copyable aria-label='Functions' }

___
### Remove·From·Orbit () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void RemoveFromOrbit ( ) {: .copyable aria-label='Functions' }

___
### Shoot () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void Shoot ( ) {: .copyable aria-label='Functions' }
When called in POST_FAMILIAR_UPDATE on a custom familiar, appears to handle everything for a basic shooting familiar. This includes handling animations, firing tears, and synergies.

## Variables
### Coins {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Coins  {: .copyable aria-label='Variables' }

___
### Fire·Cooldown {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int FireCooldown  {: .copyable aria-label='Variables' }

___
### Head·Frame·Delay {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int HeadFrameDelay  {: .copyable aria-label='Variables' }

___
### Hearts {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Hearts  {: .copyable aria-label='Variables' }

___
### Is·Delayed {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsDelayed {: .copyable aria-label='Variables' }

___
### Is·Follower {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsFollower {: .copyable aria-label='Variables' }

___
### Keys {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Keys  {: .copyable aria-label='Variables' }

___
### Last·Direction {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Direction](enums/Direction.md) LastDirection  {: .copyable aria-label='Variables' }

___
### Move·Direction {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Direction](enums/Direction.md) MoveDirection  {: .copyable aria-label='Variables' }

___
### Orbit·Angle·Offset {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float OrbitAngleOffset  {: .copyable aria-label='Variables' }

Can be used to override the angular position of the familiar on its orbit based on the initial starting position of the orbit.

???- example "Example Code"
    This code will make all of your orbitals move as a tight wall around you.

    ```lua
    for i,v in ipairs(Isaac

[TRUNCATED: 原文过长，已截断以适配上下文窗口]

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "AddCoins",
    "signature": "void AddCoins ( int Value ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "AddHearts",
    "signature": "void AddHearts ( int Hearts ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "AddKeys",
    "signature": "void AddKeys ( int Keys ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "AddToDelayed",
    "signature": "void AddToDelayed ( ) {: .copyable aria-label='Functions' }",
    "description": "Adds to delayed. This doesn't remove other flags!"
  },
  {
    "method_id": "m005",
    "name": "AddToFollowers",
    "signature": "void AddToFollowers ( ) {: .copyable aria-label='Functions' }",
    "description": "Adds to followers. This doesn't remove other flags!"
  },
  {
    "method_id": "m006",
    "name": "AddToOrbit",
    "signature": "void AddToOrbit ( int Layer ) {: .copyable aria-label='Functions' }",
    "description": "Adds to orbitals. This doesn't remove other flags!"
  },
  {
    "method_id": "m007",
    "name": "FireProjectile",
    "signature": "[EntityTear](EntityTear.md) FireProjectile ( [Vector](Vector.md) Dir ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "FollowParent",
    "signature": "void FollowParent ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "FollowPosition",
    "signature": "void FollowPosition ( [Vector](Vector.md) Pos ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "GetOrbitDistance",
    "signature": "static [Vector](Vector.md) GetOrbitDistance ( int Layer ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "GetOrbitPosition",
    "signature": "[Vector](Vector.md) GetOrbitPosition ( [Vector](Vector.md) Pos ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "MoveDelayed",
    "signature": "void MoveDelayed ( int NumFrames ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "MoveDiagonally",
    "signature": "void MoveDiagonally ( float Speed ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "PickEnemyTarget",
    "signature": "void PickEnemyTarget ( float MaxDistance, int FrameInterval = 13, int Flags = 0, [Vector](Vector.md) ConeDir = Vector.Zero, float ConeAngle = 15 ) {: .copyable aria-label='Functions' }",
    "description": "**Flags**: A combination of the following flags (none of these are set by default)"
  },
  {
    "method_id": "m015",
    "name": "PlayChargeAnim",
    "signature": "void PlayChargeAnim ( [Direction](enums/Direction.md) Dir ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m016",
    "name": "PlayFloatAnim",
    "signature": "void PlayFloatAnim ( [Direction](enums/Direction.md) Dir ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m017",
    "name": "PlayShootAnim",
    "signature": "void PlayShootAnim ( [Direction](enums/Direction.md) Dir ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m018",
    "name": "RecalculateOrbitOffset",
    "signature": "int RecalculateOrbitOffset ( int Layer, boolean Add ) {: .copyable aria-label='Functions' }",
    "description": "Returns the number of familiars in that layer."
  },
  {
    "method_id": "m019",
    "name": "RemoveFromDelayed",
    "signature": "void RemoveFromDelayed ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m020",
    "name": "RemoveFromFollowers",
    "signature": "void RemoveFromFollowers ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m021",
    "name": "RemoveFromOrbit",
    "signature": "void RemoveFromOrbit ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m022",
    "name": "Shoot",
    "signature": "void Shoot ( ) {: .copyable aria-label='Functions' }",
    "description": "When called in POST_FAMILIAR_UPDATE on a custom familiar, appears to handle everything for a basic shooting familiar. This includes handling animations, firing tears, and synergies."
  },
  {
    "method_id": "m023",
    "name": "Coins",
    "signature": "int Coins  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m024",
    "name": "FireCooldown",
    "signature": "int FireCooldown  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m025",
    "name": "HeadFrameDelay",
    "signature": "int HeadFrameDelay  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m026",
    "name": "Hearts",
    "signature": "int Hearts  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m027",
    "name": "IsDelayed",
    "signature": "boolean IsDelayed {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m028",
    "name": "IsFollower",
    "signature": "boolean IsFollower {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m029",
    "name": "Keys",
    "signature": "int Keys  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m030",
    "name": "LastDirection",
    "signature": "[Direction](enums/Direction.md) LastDirection  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m031",
    "name": "MoveDirection",
    "signature": "[Direction](enums/Direction.md) MoveDirection  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m032",
    "name": "OrbitAngleOffset",
    "signature": "float OrbitAngleOffset  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m033",
    "name": "OrbitDistance",
    "signature": "[Vector](Vector.md) OrbitDistance  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m034",
    "name": "OrbitLayer",
    "signature": "int OrbitLayer  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m035",
    "name": "OrbitSpeed",
    "signature": "float OrbitSpeed  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m036",
    "name": "Player",
    "signature": "[EntityPlayer](EntityPlayer.md) Player  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m037",
    "name": "RoomClearCount",
    "signature": "int RoomClearCount  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m038",
    "name": "ShootDirection",
    "signature": "[Direction](enums/Direction.md) ShootDirection  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m039",
    "name": "State",
    "signature": "int State  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "EntityFamiliar 控制玩家跟班，提供跟随、环绕、射击、资源存取与动画播放等功能。",
    "use_cases": [
      "自定义跟班移动和攻击模式",
      "管理跟班轨道层及状态"
    ],
    "key_methods": [
      "AddToOrbit",
      "Shoot",
      "FireProjectile",
      "FollowParent",
      "PickEnemyTarget"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "增加跟班持有的硬币数量。",
      "use_cases": [
        "调整贪婪跟班的产出"
      ],
      "key_methods": [
        "AddCoins",
        "Coins"
      ]
    },
    {
      "method_id": "m002",
      "summary": "增加跟班的心之容器。",
      "use_cases": [
        "修改跟班生命值"
      ],
      "key_methods": [
        "AddHearts",
        "Hearts"
      ]
    },
    {
      "method_id": "m003",
      "summary": "增加跟班的钥匙数量。",
      "use_cases": [
        "控制钥匙型跟班效果"
      ],
      "key_methods": [
        "AddKeys",
        "Keys"
      ]
    },
    {
      "method_id": "m004",
      "summary": "将跟班设为延迟跟随，不覆盖已有标记。",
      "use_cases": [
        "实现特殊移动轨迹"
      ],
      "key_methods": [
        "AddToDelayed",
        "RemoveFromDelayed",
        "MoveDelayed"
      ]
    },
    {
      "method_id": "m005",
      "summary": "将跟班加入跟随者列表，不消除其他标记。",
      "use_cases": [
        "切换到标准跟随模式"
      ],
      "key_methods": [
        "AddToFollowers",
        "RemoveFromFollowers"
      ]
    },
    {
      "method_id": "m006",
      "summary": "将跟班加入指定轨道层成为环绕物。",
      "use_cases": [
        "自定义环绕跟班部署"
      ],
      "key_methods": [
        "AddToOrbit",
        "RemoveFromOrbit",
        "RecalculateOrbitOffset"
      ]
    },
    {
      "method_id": "m007",
      "summary": "从跟班中心向指定方向发射普通泪弹，返回该弹实体。",
      "use_cases": [
        "手动触发攻击"
      ],
      "key_methods": [
        "FireProjectile",
        "Shoot",
        "PlayShootAnim"
      ]
    },
    {
      "method_id": "m008",
      "summary": "让跟班立即回归玩家身边标准跟随。",
      "use_cases": [
        "重置跟随位置"
      ],
      "key_methods": [
        "FollowParent",
        "FollowPosition"
      ]
    },
    {
      "method_id": "m009",
      "summary": "命令跟班移动到指定坐标。",
      "use_cases": [
        "自定义移动路径"
      ],
      "key_methods": [
        "FollowPosition",
        "FollowParent"
      ]
    },
    {
      "method_id": "m010",
      "summary": "静态方法，获取指定轨道层的基础距离向量。",
      "use_cases": [
        "计算轨道位置"
      ],
      "key_methods": [
        "GetOrbitDistance",
        "GetOrbitPosition"
      ]
    },
    {
      "method_id": "m011",
      "summary": "返回环绕跟班相对于玩家的位置，支持偏移参数。",
      "use_cases": [
        "轨道位置调试"
      ],
      "key_methods": [
        "GetOrbitPosition",
        "GetOrbitDistance"
      ]
    },
    {
      "method_id": "m012",
      "summary": "让延迟跟随的跟班在指定帧数内移动。",
      "use_cases": [
        "平滑跟随效果"
      ],
      "key_methods": [
        "MoveDelayed",
        "AddToDelayed"
      ]
    },
    {
      "method_id": "m013",
      "summary": "按给定速度沿对角线方向移动跟班。",
      "use_cases": [
        "特殊移动模式"
      ],
      "key_methods": [
        "MoveDiagonally"
      ]
    },
    {
      "method_id": "m014",
      "summary": "为跟班选择敌人目标，支持距离、优先级与视野锥形过滤。",
      "use_cases": [
        "自定义索敌逻辑"
      ],
      "key_methods": [
        "PickEnemyTarget",
        "Shoot"
      ]
    },
    {
      "method_id": "m015",
      "summary": "播放跟班的蓄力动画。",
      "use_cases": [
        "同步动画表现"
      ],
      "key_methods": [
        "PlayChargeAnim",
        "Shoot"
      ]
    },
    {
      "method_id": "m016",
      "summary": "播放跟班的漂浮动画。",
      "use_cases": [
        "自定义漂浮外观"
      ],
      "key_methods": [
        "PlayFloatAnim"
      ]
    },
    {
      "method_id": "m017",
      "summary": "播放跟班的射击动画。",
      "use_cases": [
        "同步射击表现"
      ],
      "key_methods": [
        "PlayShootAnim",
        "Shoot"
      ]
    },
    {
      "method_id": "m018",
      "summary": "重新计算轨道层的偏移并返回该层跟班数量。",
      "use_cases": [
        "动态调整环绕物布局"
      ],
      "key_methods": [
        "RecalculateOrbitOffset",
        "AddToOrbit",
        "RemoveFromOrbit"
      ]
    },
    {
      "method_id": "m019",
      "summary": "将跟班从延迟跟随列表中移除。",
      "use_cases": [
        "停止延迟跟随"
      ],
      "key_methods": [
        "RemoveFromDelayed",
        "AddToDelayed"
      ]
    },
    {
      "method_id": "m020",
      "summary": "将跟班从跟随者列表中移除。",
      "use_cases": [
        "取消标准跟随"
      ],
      "key_methods": [
        "RemoveFromFollowers",
        "AddToFollowers"
      ]
    },
    {
      "method_id": "m021",
      "summary": "将跟班从环绕列表中移除。",
      "use_cases": [
        "脱离轨道"
      ],
      "key_methods": [
        "RemoveFromOrbit",
        "AddToOrbit"
      ]
    },
    {
      "method_id": "m022",
      "summary": "执行完整射击流程：处理动画、发射泪弹和协同效果。",
      "use_cases": [
        "一键射击逻辑"
      ],
      "key_methods": [
        "Shoot",
        "FireProjectile",
        "PlayShootAnim"
      ]
    },
    {
      "method_id": "m023",
      "summary": "跟班当前硬币数量的读写变量。",
      "use_cases": [
        "读取/设置硬币增益"
      ],
      "key_methods": [
        "Coins",
        "AddCoins"
      ]
    },
    {
      "method_id": "m024",
      "summary": "射击冷却计时器变量。",
      "use_cases": [
        "控制攻击间隔"
      ],
      "key_methods": [
        "FireCooldown",
        "Shoot"
      ]
    },
    {
      "method_id": "m025",
      "summary": "头部动画帧延迟变量。",
      "use_cases": [
        "调整头部动画速度"
      ],
      "key_methods": [
        "HeadFrameDelay"
      ]
    },
    {
      "method_id": "m026",
      "summary": "跟班当前心数变量。",
      "use_cases": [
        "跟班生命值管理"
      ],
      "key_methods": [
        "Hearts",
        "AddHearts"
      ]
    },
    {
      "method_id": "m027",
      "summary": "布尔值，指示跟班是否处于延迟跟随状态。",
      "use_cases": [
        "状态查询"
      ],
      "key_methods": [
        "Is
```
