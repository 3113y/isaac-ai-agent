# DeepSeek Context

- class: EntityFamiliar
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 10950
- temperature: 0.2
- timestamp: 2026-04-29T14:39:37.907931

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
    for i,v in ipairs(Isaac.GetRoomEntities()) do
        if v.Type==3 then
            v:ToFamiliar().OrbitAngleOffset = 0.25*i
        end
    end
    ```

    Result: ![angle offset](images/example_familiar_angleOffset.png)
___
### Orbit·Distance {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) OrbitDistance  {: .copyable aria-label='Variables' }

Defines the orbit of the familiar, if its an orbital. The Vector is interpreted as the dimensions of the circle/oval orbit. Example: `:::lua Vector(110,90)` is the orbital of "Forever alone".
___
### Orbit·Layer {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int OrbitLayer  {: .copyable aria-label='Variables' }

This value is `-1` by default, and changes to whichever value is defined by `EntityFamiliar:AddToOrbit()`.
___
### Orbit·Speed {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float OrbitSpeed  {: .copyable aria-label='Variables' }

___
### Player {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [EntityPlayer](EntityPlayer.md) Player  {: .copyable aria-label='Variables' }

___
### Room·Clear·Count {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int RoomClearCount  {: .copyable aria-label='Variables' }

___
### Shoot·Direction {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Direction](enums/Direction.md) ShootDirection  {: .copyable aria-label='Variables' }

___
### State {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int State  {: .copyable aria-label='Variables' }

___

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
    "summary": "Represents a familiar entity that can follow the player, orbit, shoot tears, collect pickups, and be managed as part of follower/delayed/orbit groups. Provides controls for movement, targeting, animation, and state.",
    "use_cases": [
      "Creating custom familiars with shooting and movement behavior",
      "Managing orbital layouts and positions",
      "Controlling delayed or follower status for familiar grouping",
      "Customizing targeting logic for offensive familiars",
      "Reading/writing familiar-specific stats like coins, hearts, keys"
    ],
    "key_methods": [
      "Shoot",
      "AddToOrbit",
      "AddToFollowers",
      "FireProjectile",
      "PickEnemyTarget"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "Increases the familiar's coin count.",
      "use_cases": [
        "Accumulating coins for coin-based familiars",
        "Custom pickup management"
      ],
      "key_methods": [
        "AddCoins",
        "Coins"
      ]
    },
    {
      "method_id": "m002",
      "summary": "Increases the familiar's heart count.",
      "use_cases": [
        "Healing or health-based familiar mechanics",
        "Custom health pickup simulation"
      ],
      "key_methods": [
        "AddHearts",
        "Hearts"
      ]
    },
    {
      "method_id": "m003",
      "summary": "Increases the familiar's key count.",
      "use_cases": [
        "Key-based familiar behaviors",
        "Simulating key collection"
      ],
      "key_methods": [
        "AddKeys",
        "Keys"
      ]
    },
    {
      "method_id": "m004",
      "summary": "Adds the familiar to the delayed movement set without removing other flags, enabling delayed follow behavior.",
      "use_cases": [
        "Enabling delayed movement like Tractor Beam effect",
        "Layering movement states"
      ],
      "key_methods": [
        "AddToDelayed",
        "RemoveFromDelayed",
        "MoveDelayed",
        "IsDelayed"
      ]
    },
    {
      "method_id": "m005",
      "summary": "Adds the familiar to the followers group, making it a normal follower without clearing other flags.",
      "use_cases": [
        "Setting a familiar as a standard follower",
        "Re‑enabling follower status after orbital or delayed use"
      ],
      "key_methods": [
        "AddToFollowers",
        "RemoveFromFollowers",
        "IsFollower",
        "FollowParent"
      ]
    },
    {
      "method_id": "m006",
      "summary": "Adds the familiar to an orbital layer, setting it to orbit the player without removing other flags.",
      "use_cases": [
        "Converting a familiar into an orbital",
        "Stacking orbitals in specific layers"
      ],
      "key_methods": [
        "AddToOrbit",
        "RemoveFromOrbit",
        "OrbitLayer",
        "GetOrbitPosition",
        "RecalculateOrbitOffset"
      ]
    },
    {
      "method_id": "m007",
      "summary": "Shoots a regular tear from the familiar's center in the given direction. Returns the leftmost projectile; does not play shoot animation or use special attacks.",
      "use_cases": [
        "Custom projectile attacks",
        "Testing basic tear firing without side effects"
      ],
      "key_methods": [
        "FireProjectile",
        "Shoot",
        "PlayShootAnim"
      ]
    },
    {
      "method_id": "m008",
      "summary": "Makes the familiar follow its parent (player) like a default follower.",
      "use_cases": [
        "Restoring normal following behavior",
        "Initializing follower movement"
      ],
      "key_methods": [
        "FollowParent",
        "FollowPosition",
        "AddToFollowers"
      ]
    },
    {
      "method_id": "m009",
      "summary": "Moves the familiar towards a specific world position.",
      "use_cases": [
        "Custom movement patterns",
        "Teleporting or repositioning a familiar"
      ],
      "key_methods": [
        "FollowPosition",
        "FollowParent",
        "MoveDiagonally"
      ]
    },
    {
      "method_id": "m010",
      "summary": "Static method returning the default orbit distance vector for a given orbital layer.",
      "use_cases": [
        "Getting baseline orbit dimensions",
        "Orbit calculations without an instance"
      ],
      "key_methods": [
        "GetOrbitDistance",
        "OrbitDistance",
        "AddToOrbit",
        "GetOrbitPosition"
      ]
    },
    {
      "method_id": "m011",
      "summary": "Returns the world position of an orbiting familiar relative to the player, with an offset.",
      "use_cases": [
        "Drawing custom orbital effects",
        "Precise orbital targeting"
      ],
      "key_methods": [
        "GetOrbitPosition",
        "AddToOrbit",
        "OrbitDistance"
      ]
    },
    {
      "method_id": "m012",
      "summary": "Incrementally moves the familiar in its delayed state over a number of frames.",
      "use_cases": [
        "Smooth delayed repositioning",
        "Controlling Tractor Beam-like movement"
      ],
      "key_methods": [
        "MoveDelayed",
        "AddToDelayed",
        "RemoveFromDelayed"
      ]
    },
    {
      "method_id": "m013",
      "summary": "Moves the familiar diagonally at a given speed.",
      "use_cases": [
        "Custom movement patterns",
        "Evasive or attack maneuvers"
      ],
      "key_methods": [
        "MoveDiagonally",
        "FollowPosition",
        "FollowParent"
      ]
    },
    {
      "method_id": "m014",
      "summary": "Selects an enemy target based on distance, interval, and optional flags/cone constraints. Can prioritize switching, HP, or owner proximity.",
      "use_cases": [
        "Advanced familiar AI targeting",
        "Cone‑based attack logic"
      ],
      "key_methods": [
        "PickEnemyTarget",
        "FireProjectile",
        "Shoot"
      ]
    },
    {
      "method_id": "m015",
      "summary": "Plays the charge animation in the specified direction.",
      "use_cases": [
        "Custom charging attack visuals",
        "Synchronizing animation with mechanics"
      ],
      "key_methods": [
        "PlayChargeAnim",
        "PlayShootAnim",
        "Shoot"
      ]
    },
    {
      "method_id": "m016",
      "summary": "Plays the float (idle/movement) animation in the specified direction.",
      "use_cases": [
        "Custom idle or floating animations",
        "State‑based visual feedback"
      ],
      "key_methods": [
        "PlayFloatAnim",
        "PlayChargeAnim",
        "PlayShootAnim"
      ]
    },
    {
      "method_id": "m017",
      "summary": "Plays the shoot animation in the specified direction.",
      "use_cases": [
        "Triggering shoot visuals manually",
        "Cosmetic familiar customization"
      ],
      "key_methods": [
        "PlayShootAnim",
        "Shoot",
        "FireProjectile"
      ]
    },
    {
      "method_id": "m018",
      "summary": "Recalculates the orbital offset for a given layer, optionally adding the familiar to it. Returns the total number of familiars in that layer.",
      "use_cases": [
        "Adjusting orbital spacing dynamically",
        "Managing layered orbital groups"
      ],
      "key_methods": [
        "RecalculateOrbitOffset",
        "AddToOrbit",
        "RemoveFromOrbit",
        "OrbitLayer"
      ]
    },
    {
      "method_id": "m019",
      "summary": "Removes the familiar from the delayed movement set.",
      "use_cases": [
        "Disabling delayed behavior",
        "Switching movement modes"
      ],
      "key_methods": [
        "RemoveFromDelayed",
        "AddToDelayed",
        "IsDelayed"
      ]
    },
    {
      "method_id": "m020",
      "summary": "Removes the familiar from the followers list.",
      "use_cases": [
        "Temporarily detaching a follower",
        "Switching to orbital or other state"
      ],
      "key_methods": [
        "RemoveFromFollowers",
        "AddToFollowers",
        "IsFollower"
      ]
    },
    {
      "method_id": "m021",
      "summary": "Removes the familiar from its orbital layer.",
      "use_cases": [
        "Taking an orbital out of orbit",
        "Switching to follower mode"
      ],
      "key_methods": [
        "RemoveFromOrbit",
        "AddToOrbit",
        "OrbitLayer"
      ]
    },
    {
      "method_id": "m022",
      "summary": "Handles the complete shooting routine for a basic shooting familiar: animations, tear firing, and synergy processing. Recommended for custom familiars in POST_FAMILIAR_UPDATE.",
      "use_cases": [
        "Implementing a standard shooting familiar",
        "Centralizing shoot logic with automatic synergy support"
      ],
      "key_methods": [
        "Shoot",
        "FireProjectile",
        "PlayShootAnim",
        "FireCooldown"
      ]
    },
    {
      "method_id": "m023",
      "summary": "Variable: Current coin count of the familiar.",
      "use_cases": [
        "Reading/modifying coin amount for coin-based familiar logic",
        "Custom pickup display"
      ],
      "key_methods": [
        "Coins",
        "AddCoins"
      ]
    },
    {
      "method_id": "m024",
      "summary": "Variable: Cooldown timer before the familiar can shoot again.",
      "use_cases": [
        "Adjusting fire rate",
        "Synchronizing custom shoot logic"
      ],
      "key_methods": [
        "FireCooldown",
        "Shoot",
        "FireProjectile"
      ]
    },
    {
      "method_id": "m025",
      "summary": "Variable: Frame delay for the familiar's head animation.",
      "use_cases": [
        "Custom animation timing",
        "Head‑based familiar behavior"
      ],
      "key_methods": [
        "HeadFrameDelay"
      ]
    },
    {
      "method_id": "m026",
      "summary": "Variable: Current heart count of the familiar.",
      "use_cases": [
        "Health‑based familiar mechanics",
        "Custom heart pickup tracking"
      ],
      "key_methods": [
        "Hearts",
        "AddHearts"
      ]
    },
    {
      "method_id": "m027",
      "summary": "Variable: Whether the familiar is in the delayed movement set.",
      "use_cases": [
        "Checking movement state",
        "Conditional behavior based on delayed status"
      ],
      "key_methods": [
        "IsDelayed",
        "AddToDelayed",
        "RemoveFromDelayed"
      ]
    },
    {
      "method_id": "m028",
      "summary": "Variable: Whether the familiar is currently registered as a follower.",
      "use_cases": [
        "State queries for follower‑only logic",
        "Determining if the familiar follows the player"
      ],
      "key_methods": [
        "IsFollower",
        "AddToFollowers",
        "RemoveFromFollowers"
      ]
    },
    {
      "method_id": "m029",
      "summary": "Variable: Current key count of the familiar.",
      "use_cases": [
        "Key‑based familiar interactions",
        "Tracking key pickups"
      ],
      "key_methods": [
        "Keys",
        "AddKeys"
      ]
    },
    {
      "method_id": "m030",
      "summary": "Variable: The last movement direction of the familiar.",
      "use_cases": [
        "Storing previous direction for animation or AI",
        "Detecting direction changes"
      ],
      "key_methods": [
        "LastDirection",
        "MoveDirection"
      ]
    },
    {
      "method_id": "m031",
      "summary": "Variable: The current movement direction of the familiar.",
      "use_cases": [
        "Reading active movement vector",
        "Custom controller input mapping"
      ],
      "key_methods": [
        "MoveDirection",
        "LastDirection"
      ]
    },
    {
      "method_id": "m032",
      "summary": "Variable: Angular offset for the familiar on its orbit, allowing manual repositioning along the orbital path.",
      "use_cases": [
        "Creating tight orbital walls",
        "Custom orbital arrangements"
      ],
      "key_methods": [
        "OrbitAngleOffset",
        "AddToOrbit",
        "GetOrbitPosition"
      ]
    },
    {
      "method_id": "m033",
      "summary": "Variable: Defines the orbit dimensions as a Vector (width, height) when the familiar is an orbital.",
      "use_cases": [
        "Setting custom orbital shapes",
        "Dynamic orbit resizing"
      ],
      "key_methods": [
        "OrbitDistance",
        "AddToOrbit",
        "GetOrbitDistance"
      ]
    },
    {
      "method_id": "m034",
      "summary": "Variable: The orbital layer index (‑1 if not an orbital). Set by AddToOrbit.",
      "use_cases": [
        "Identifying orbital layer",
        "Layer‑based filtering"
      ],
      "key_methods": [
        "OrbitLayer",
        "AddToOrbit",
        "RemoveFromOrbit",
        "RecalculateOrbitOffset"
      ]
    },
    {
      "method_id": "m035",
      "summary": "Variable: Speed at which the familiar moves along its orbit.",
      "use_cases": [
        "Adjusting orbital rotation speed",
        "Creating custom orbit dynamics"
      ],
      "key_methods": [
        "OrbitSpeed",
        "AddToOrbit"
      ]
    },
    {
      "method_id": "m036",
      "summary": "Variable: Reference to the EntityPlayer that owns this familiar.",
      "use_cases": [
        "Accessing player stats for familiar syncing",
        "Checking owner properties"
      ],
      "key_methods": [
        "Player",
        "FollowParent"
      ]
    },
    {
      "method_id": "m037",
      "summary": "Variable: Tracks the number of room clears, possibly related to familiar progression.",
      "use_cases": [
        "Unlocking behaviors after certain clears",
        "Room‑clear‑dependent logic"
      ],
      "key_methods": [
        "RoomClearCount"
      ]
    },
    {
      "method_id": "m038",
      "summary": "Variable: The direction in which the familiar is shooting.",
      "use_cases": [
        "Reading current shoot aim",
        "Aligning visual effects with shoot direction"
      ],
      "key_methods": [
        "ShootDirection",
        "Shoot",
        "FireProjectile"
      ]
    },
    {
      "method_id": "m039",
      "summary": "Variable: The AI state integer, used to control familiar behavior stages.",
      "use_cases": [
        "Custom state machines for familiars",
        "Synchronizing behavior with state"
      ],
      "key_methods": [
        "State",
        "Shoot"
      ]
    }
  ]
}
```
