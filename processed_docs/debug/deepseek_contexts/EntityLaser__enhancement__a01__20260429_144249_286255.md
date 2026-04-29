# DeepSeek Context

- class: EntityLaser
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 12200
- temperature: 0.2
- timestamp: 2026-04-29T14:42:49.286300

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

类名：EntityLaser

原始 md 文档（该类完整文档，可能已截断）：
# Class "EntityLaser"

???+ info
    You can get this class by using the following function:

    * [Entity.ToLaser()](Entity.md#tolaser)
    * [EntityPlayer.FireBrimstone()](EntityPlayer.md#firebrimstone)
    * [EntityPlayer.FireDelayedBrimstone()](EntityPlayer.md#firedelayedbrimstone)
    * [EntityPlayer.FireTechLaser()](EntityPlayer.md#firetechlaser)
    * [EntityPlayer.FireTechXLaser()](EntityPlayer.md#firetechxlaser)

    ???+ example "Example Code"
        `local brimstoneEntity = Isaac.GetPlayer():FireBrimstone(Vector(1, 0))`

## Class Diagram
--8<-- "docs/snippets/EntityClassDiagram.md"
## Functions
### Add·Tear·Flags () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }

___
### Calculate·End·Point () {: aria-label='Functions' }
[ ](#){: .static .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### static [Vector](Vector.md) CalculateEndPoint ( [Vector](Vector.md) Start, [Vector](Vector.md) Dir, [Vector](Vector.md) PositionOffset, [Entity](Entity.md) Parent, float Margin ) {: .copyable aria-label='Functions' }

___
### Clear·Tear·Flags () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void ClearTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }

___
### Get·End·Point () {: aria-label='Functions' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [Vector](Vector.md) GetEndPoint ( ) {: .copyable aria-label='Functions' }

___
### Get·Non·Optimized·Samples () {: aria-label='Functions' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [VectorList](CppContainer_Vector_VectorList.md) GetNonOptimizedSamples ( ) {: .copyable aria-label='Functions' }
返回一个向量表（VectorList）用于表达激光的路径。通常会返回沿激光路径均匀分布的51个点，相对于[`GetSamples()`](#getsamples)只返回表示激光路径所需的最少点。

???+ example "Example Usage"
    ```lua
    local samplePoints = laser:GetNonOptimizedSamples()

    for i=0, #samplePoints-1 do
        local pos = samplePoints:Get(i)
        ...
    end
    ```

___
### Get·Render·Z () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### int GetRenderZ ( ) {: .copyable aria-label='Functions' }

___
### Get·Samples () {: aria-label='Functions' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [VectorList](CppContainer_Vector_VectorList.md) GetSamples ( ) {: .copyable aria-label='Functions' }

返回一个向量表（VectorList）表示激光的路径。与 [`GetNonOptimizedSamples()`](#getnonoptimizedsamples) 不同，此函数返回尽可能少的点，同时仍然正确表示激光的路径。

例如，对于完全直的激光，[`GetNonOptimizedSamples()`](#getnonoptimizedsamples) 将始终返回 51 个点，但此函数仅返回 2 个。

???+ example "Example Usage"
    ```lua
    local samplePoints = laser:GetSamples()

    for i=0, #samplePoints-1 do
        local pos = samplePoints:Get(i)
        ...
    end
    ```

___
### Has·Tear·Flags () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean HasTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }

___
### Is·Circle·Laser () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsCircleLaser ( ) {: .copyable aria-label='Functions' }

???- note "Note"
    此函数无法区分不同类型的圆形激光，但可以通过其子类型进行识别：

    * 0 - 线性激光（典型的激光，具有起点和终点）
    * 1 - 环形鲁多维科（用于鲁多维科科技协同的受控激光环）
    * 2 - 环形投射物（科技X）
    * 3 - 环形跟随父物体（虚空之喉）
    * 4 - 无碰撞（无碰撞溅射，例如科技零）

___
### Is·Sample·Laser () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsSampleLaser ( ) {: .copyable aria-label='Functions' }

___
### Set·Active·Rotation () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetActiveRotation ( int Delay, float AngleDegrees, float RotationSpd, boolean TimeoutComplete ) {: .copyable aria-label='Functions' }

___
### Set·Black·Hp·Drop·Chance () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetBlackHpDropChance ( float Chance ) {: .copyable aria-label='Functions' }

___
### Set·Homing·Type () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetHomingType ( LaserHomingType Type ) {: .copyable aria-label='Functions' }

___
### Set·Max·Distance () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetMaxDistance ( float Distance ) {: .copyable aria-label='Functions' }

___
### Set·Multidimensional·Touched () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetMultidimensionalTouched ( boolean Value ) {: .copyable aria-label='Functions' }

___
### Set·One·Hit () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetOneHit ( boolean Value ) {: .copyable aria-label='Functions' }

___
### Set·Timeout () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetTimeout ( int Value ) {: .copyable aria-label='Functions' }

___
### Shoot·Angle () {: aria-label='Functions' }
[ ](#){: .static .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### static [EntityLaser](EntityLaser.md) ShootAngle ( int Variant, [Vector](Vector.md) SourcePos, float AngleDegrees, int Timeout, [Vector](Vector.md) PosOffset, [Entity](Entity.md) Source ) {: .copyable aria-label='Functions' }
简单化静态助手以简化激光的生成
___
## Variables
### Angle {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Angle  {: .copyable aria-label='Variables' }

___
### Angle·Degrees {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float AngleDegrees  {: .copyable aria-label='Variables' }

___
### Black·Hp·Drop·Chance {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float BlackHpDropChance  {: .copyable aria-label='Variables' }
For maw of void.
___
### Bounce·Laser {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Entity](Entity.md) BounceLaser  {: .copyable aria-label='Variables' data-altreturn='nil' }

___
### Curve·Strength {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float CurveStrength  {: .copyable aria-label='Variables' }
My Reflection.
___
### Disable·Follow·Parent {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean DisableFollowParent  {: .copyable aria-label='Variables' }
设置为其他激光的子项时使用，例如橡胶胶水的反弹。禁用 m_ParentOffset。
___
### End·Point {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) EndPoint  {: .copyable aria-label='Variables' }
将会保存终点，以便在外部访问时不需要重新计算。
___
### First·Update {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean FirstUpdate  {: .copyable aria-label='Variables' }

___
### Grid·Hit {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean GridHit  {: .copyable aria-label='Variables' }
返回 `true` 如果激光可以被网格实体阻挡，并且在该帧被阻挡。
___
### Homing·Laser {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### HomingLaser HomingLaser  {: .copyable aria-label='Variables' }

___
### Homing·Type {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### LaserHomingType HomingType  {: .copyable aria-label='Variables' }

___
### Is·Active·Rotating {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsActiveRotating  {: .copyable aria-label='Variables' }

___
### Laser·Length {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float LaserLength  {: .copyable aria-label='Variables' }

___
### Last·Angle·Degrees {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float LastAngleDegrees  {: .copyable aria-label='Variables' }

___
### Max·Distance {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float MaxDistance  {: .copyable aria-label='Variables' }
Used to trim brimstone for Azazel (0 - off)
___
### One·Hit {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean OneHit  {: .copyable aria-label='Variables' }
Laser hits only once.
___
### Parent·Offset {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) ParentOffset  {: .copyable aria-label='Variables' }

___
### Radius {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Radius  {: .copyable aria-label='Variables' }

___
### Rotation·Degrees {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float RotationDegrees  {: .copyable aria-label='Variables' }

___
### Rotation·Delay {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int RotationDelay  {: .copyable aria-label='Variables' }

___
### Rotation·Spd {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float RotationSpd  {: .copyable aria-label='Variables' }

___
### Sample·Laser {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean SampleLaser  {: .copyable aria-label='Variables' }

___
### Shrink {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean Shrink  {: .copyable aria-label='Variables' }

___
### Start·Angle·Degrees {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float StartAngleDegrees  {: .copyable aria-label='Variables' }

一些激光在旋转时会有随机变化，因此它们需要记住起始点。
___
### Tear·Flags {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [TearFlags](enums/TearFlags.md) TearFlags  {: .copyable aria-label='Variables' }
___
### Timeout {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Timeout  {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "AddTearFlags",
    "signature": "void AddTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "CalculateEndPoint",
    "signature": "static [Vector](Vector.md) CalculateEndPoint ( [Vector](Vector.md) Start, [Vector](Vector.md) Dir, [Vector](Vector.md) PositionOffset, [Entity](Entity.md) Parent, float Margin ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "ClearTearFlags",
    "signature": "void ClearTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "GetEndPoint",
    "signature": "const [Vector](Vector.md) GetEndPoint ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "GetNonOptimizedSamples",
    "signature": "const [VectorList](CppContainer_Vector_VectorList.md) GetNonOptimizedSamples ( ) {: .copyable aria-label='Functions' }",
    "description": "返回一个向量表（VectorList）用于表达激光的路径。通常会返回沿激光路径均匀分布的51个点，相对于[`GetSamples()`](#getsamples)只返回表示激光路径所需的最少点。"
  },
  {
    "method_id": "m006",
    "name": "GetRenderZ",
    "signature": "int GetRenderZ ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "GetSamples",
    "signature": "const [VectorList](CppContainer_Vector_VectorList.md) GetSamples ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "HasTearFlags",
    "signature": "boolean HasTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "IsCircleLaser",
    "signature": "boolean IsCircleLaser ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "IsSampleLaser",
    "signature": "boolean IsSampleLaser ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "SetActiveRotation",
    "signature": "void SetActiveRotation ( int Delay, float AngleDegrees, float RotationSpd, boolean TimeoutComplete ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "SetBlackHpDropChance",
    "signature": "void SetBlackHpDropChance ( float Chance ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "SetHomingType",
    "signature": "void SetHomingType ( LaserHomingType Type ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "SetMaxDistance",
    "signature": "void SetMaxDistance ( float Distance ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "SetMultidimensionalTouched",
    "signature": "void SetMultidimensionalTouched ( boolean Value ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m016",
    "name": "SetOneHit",
    "signature": "void SetOneHit ( boolean Value ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m017",
    "name": "SetTimeout",
    "signature": "void SetTimeout ( int Value ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m018",
    "name": "ShootAngle",
    "signature": "static [EntityLaser](EntityLaser.md) ShootAngle ( int Variant, [Vector](Vector.md) SourcePos, float AngleDegrees, int Timeout, [Vector](Vector.md) PosOffset, [Entity](Entity.md) Source ) {: .copyable aria-label='Functions' }",
    "description": "简单化静态助手以简化激光的生成"
  },
  {
    "method_id": "m019",
    "name": "Angle",
    "signature": "float Angle  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m020",
    "name": "AngleDegrees",
    "signature": "float AngleDegrees  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m021",
    "name": "BlackHpDropChance",
    "signature": "float BlackHpDropChance  {: .copyable aria-label='Variables' }",
    "description": "For maw of void."
  },
  {
    "method_id": "m022",
    "name": "BounceLaser",
    "signature": "[Entity](Entity.md) BounceLaser  {: .copyable aria-label='Variables' data-altreturn='nil' }",
    "description": ""
  },
  {
    "method_id": "m023",
    "name": "CurveStrength",
    "signature": "float CurveStrength  {: .copyable aria-label='Variables' }",
    "description": "My Reflection."
  },
  {
    "method_id": "m024",
    "name": "DisableFollowParent",
    "signature": "boolean DisableFollowParent  {: .copyable aria-label='Variables' }",
    "description": "设置为其他激光的子项时使用，例如橡胶胶水的反弹。禁用 m_ParentOffset。"
  },
  {
    "method_id": "m025",
    "name": "EndPoint",
    "signature": "[Vector](Vector.md) EndPoint  {: .copyable aria-label='Variables' }",
    "description": "将会保存终点，以便在外部访问时不需要重新计算。"
  },
  {
    "method_id": "m026",
    "name": "FirstUpdate",
    "signature": "boolean FirstUpdate  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m027",
    "name": "GridHit",
    "signature": "boolean GridHit  {: .copyable aria-label='Variables' }",
    "description": "返回 `true` 如果激光可以被网格实体阻挡，并且在该帧被阻挡。"
  },
  {
    "method_id": "m028",
    "name": "HomingLaser",
    "signature": "HomingLaser HomingLaser  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m029",
    "name": "HomingType",
    "signature": "LaserHomingType HomingType  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m030",
    "name": "IsActiveRotating",
    "signature": "boolean IsActiveRotating  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m031",
    "name": "LaserLength",
    "signature": "float LaserLength  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m032",
    "name": "LastAngleDegrees",
    "signature": "float LastAngleDegrees  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m033",
    "name": "MaxDistance",
    "signature": "float MaxDistance  {: .copyable aria-label='Variables' }",
    "description": "Used to trim brimstone for Azazel (0 - off)"
  },
  {
    "method_id": "m034",
    "name": "OneHit",
    "signature": "boolean OneHit  {: .copyable aria-label='Variables' }",
    "description": "Laser hits only once."
  },
  {
    "method_id": "m035",
    "name": "ParentOffset",
    "signature": "[Vector](Vector.md) ParentOffset  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m036",
    "name": "Radius",
    "signature": "float Radius  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m037",
    "name": "RotationDegrees",
    "signature": "float RotationDegrees  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m038",
    "name": "RotationDelay",
    "signature": "int RotationDelay  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m039",
    "name": "RotationSpd",
    "signature": "float RotationSpd  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m040",
    "name": "SampleLaser",
    "signature": "boolean SampleLaser  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m041",
    "name": "Shrink",
    "signature": "boolean Shrink  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m042",
    "name": "StartAngleDegrees",
    "signature": "float StartAngleDegrees  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m043",
    "name": "TearFlags",
    "signature": "[TearFlags](enums/TearFlags.md) TearFlags  {: .copyable aria-label='Variables' }",
    "description": "___"
  },
  {
    "method_id": "m044",
    "name": "Timeout",
    "signature": "int Timeout  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "EntityLaser 表示游戏中的激光实体，包括硫磺火、科技激光、环形激光等，提供对激光路径、状态、行为和属性的完整控制，常通过 EntityPlayer 的 Fire 系方法获取。",
    "use_cases": [
      "创建自定义激光攻击",
      "控制激光旋转或追踪行为",
      "获取激光路径采样点以进行碰撞检测或特效",
      "修改激光的最大距离、泪弹标志等属性",
      "判断激光类型（圆形激光等）"
    ],
    "key_methods": [
      "ShootAngle",
      "GetSamples",
      "GetEndPoint",
      "SetMaxDistance",
      "IsCircleLaser"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "将指定的TearFlags添加到激光的泪弹标志中，影响激光的碰撞或行为属性。",
      "use_cases": [
        "赋予激光穿透效果",
        "设置激光的追踪属性",
        "组合多种泪弹效果"
      ],
      "key_methods": [
        "AddTearFlags",
        "HasTearFlags",
        "ClearTearFlags",
        "TearFlags"
      ]
    },
    {
      "method_id": "m002",
      "summary": "根据起点、方向、偏移、父实体和边距计算激光的终点位置。",
      "use_cases": [
        "预先确定激光路径",
        "用于精确的碰撞预测",
        "辅助自定义激光行为"
      ],
      "key_methods": [
        "CalculateEndPoint",
        "GetEndPoint",
        "ShootAngle"
      ]
    },
    {
      "method_id": "m003",
      "summary": "移除激光的指定TearFlags，以撤销之前添加的属性。",
      "use_cases": [
        "移除追踪效果",
        "重置激光特性",
        "动态调整激光行为"
      ],
      "key_methods": [
        "ClearTearFlags",
        "AddTearFlags",
        "HasTearFlags",
        "TearFlags"
      ]
    },
    {
      "method_id": "m004",
      "summary": "返回激光的终点向量，避免重复计算，可直接用于效果定位。",
      "use_cases": [
        "获取激光末端位置",
        "在终点生成特效",
        "检测激光是否接触边界"
      ],
      "key_methods": [
        "GetEndPoint",
        "CalculateEndPoint",
        "EndPoint"
      ]
    },
    {
      "method_id": "m005",
      "summary": "返回沿激光路径均匀分布的51个样本点，即使直线也返回全量点，适合需要密集路径信息的情况。",
      "use_cases": [
        "绘制激光光柱特效",
        "精细的碰撞检测",
        "逐点处理路径事件"
      ],
      "key_methods": [
        "GetNonOptimizedSamples",
        "GetSamples"
      ]
    },
    {
      "method_id": "m006",
      "summary": "返回激光的渲染层级，用于控制绘制顺序。",
      "use_cases": [
        "调试激光绘制遮挡",
        "自定义特效渲染层级"
      ],
      "key_methods": [
        "GetRenderZ"
      ]
    },
    {
      "method_id": "m007",
      "summary": "返回表示激光路径的最少样本点，直线时仅返回起点和终点，节省计算。",
      "use_cases": [
        "高效绘制激光",
        "简化碰撞判断",
        "路径信息提取"
      ],
      "key_methods": [
        "GetSamples",
        "GetNonOptimizedSamples"
      ]
    },
    {
      "method_id": "m008",
      "summary": "测试激光当前的TearFlags是否包含给定的标志位组合。",
      "use_cases": [
        "判断激光拥有哪些属性",
        "条件逻辑分支"
      ],
      "key_methods": [
        "HasTearFlags",
        "AddTearFlags",
        "ClearTearFlags",
        "TearFlags"
      ]
    },
    {
      "method_id": "m009",
      "summary": "返回激光是否为某种环形激光（如科技X、鲁多维科环），根据子类型区分类别。",
      "use_cases": [
        "识别激光类型",
        "针对环形激光应用特殊逻辑"
      ],
      "key_methods": [
        "IsCircleLaser",
        "SetActiveRotation",
        "RotationDegrees"
      ]
    },
    {
      "method_id": "m010",
      "summary": "返回激光是否采用采样模式渲染。",
      "use_cases": [
        "区分渲染方式",
        "优化绘制策略"
      ],
      "key_methods": [
        "IsSampleLaser",
        "SampleLaser"
      ]
    },
    {
      "method_id": "m011",
      "summary": "配置激光的延迟、角度、旋转速度和超时完成标志，让激光按设定动态旋转。",
      "use_cases": [
        "创建旋转激光如科技零",
        "控制虚空之喉转动"
      ],
      "key_methods": [
        "SetActiveRotation",
        "IsActiveRotating",
        "RotationDelay",
        "RotationSpd",
        "RotationDegrees"
      ]
    },
    {
      "method_id": "m012",
      "summary": "设定激光击杀敌人掉落黑心的几率，主要用于虚空之喉。",
      "use_cases": [
        "模仿虚空之喉效果",
        "自定义掉落物逻辑"
      ],
      "key_methods": [
        "SetBlackHpDropChance",
        "BlackHpDropChance"
      ]
    },
    {
      "method_id": "m013",
      "summary": "指定激光的追踪模式（如无追踪、追踪敌人等）。",
      "use_cases": [
        "赋予激光追踪能力",
        "改变追踪行为"
      ],
      "key_methods": [
        "SetHomingType",
        "HomingType",
        "HomingLaser"
      ]
    },
    {
      "method_id": "m014",
      "summary": "限制激光的长度，如用于缩短阿萨谢尔硫磺火的最大射程。",
      "use_cases": [
        "裁剪激光距离",
        "模拟短射程激光"
      ],
      "key_methods": [
        "SetMaxDistance",
        "MaxDistance",
        "LaserLength"
      ]
    },
    {
      "method_id": "m015",
      "summary": "标记激光是否被多维伤害触发过。",
      "use_cases": [
        "管理多维效果交互",
        "防止重复触发"
      ],
      "key_methods": [
        "SetMultidimensionalTouched"
      ]
    },
    {
      "method_id": "m016",
      "summary": "使激光在命中后消失或只造成一次伤害。",
      "use_cases": [
        "创建一次性激光",
        "平衡高强度激光"
      ],
      "key_methods": [
        "SetOneHit",
        "OneHit"
      ]
    },
    {
      "method_id": "m017",
      "summary": "设定激光的存活时间帧数，到期后自动移除。",
      "use_cases": [
        "控制激光持续时间",
        "防止无限持续时间"
      ],
      "key_methods": [
        "SetTimeout",
        "Timeout",
        "FirstUpdate"
      ]
    },
    {
      "method_id": "m018",
      "summary": "简便地创建激光实体，指定类型、起点、角度、超时等参数，返回生成的激光。",
      "use_cases": [
        "快速生成自定义激光",
        "替代冗长的生成逻辑"
      ],
      "key_methods": [
        "ShootAngle",
        "CalculateEndPoint"
      ]
    },
    {
      "method_id": "m019",
      "summary": "激光当前弧度角。",
      "use_cases": [
        "读取或修改激光方向（弧度）",
        "与角度制计算转换"
      ],
      "key_methods": [
        "Angle",
        "AngleDegrees",
        "SetActiveRotation"
      ]
    },
    {
      "method_id": "m020",
      "summary": "激光当前角度（度），与Angle对应。",
      "use_cases": [
        "获取角度制方向",
        "设置旋转角度"
      ],
      "key_methods": [
        "AngleDegrees",
        "Angle",
        "SetActiveRotation"
      ]
    },
    {
      "method_id": "m021",
      "summary": "激光击杀敌人掉落黑心的概率，主要用于虚空之喉。",
      "use_cases": [
        "获取或修改黑心掉落率",
        "自定义虚空之喉行为"
      ],
      "key_methods": [
        "BlackHpDropChance",
        "SetBlackHpDropChance"
      ]
    },
    {
      "method_id": "m022",
      "summary": "指向反弹激光实体的引用，用于橡胶胶水等效果。",
      "use_cases": [
        "追踪激光反弹链",
        "管理子激光"
      ],
      "key_methods": [
        "BounceLaser",
        "DisableFollowParent"
      ]
    },
    {
      "method_id": "m023",
      "summary": "激光的弯曲强度，实现“我的倒影”效果。",
      "use_cases": [
        "制造弯曲激光",
        "模拟反射效果"
      ],
      "key_methods": [
        "CurveStrength"
      ]
    },
    {
      "method_id": "m024",
      "summary": "是否禁用跟随父对象偏移，在作为子激光时使用。",
      "use_cases": [
        "管理反弹激光的跟随",
        "解除父级依赖"
      ],
      "key_methods": [
        "DisableFollowParent",
        "ParentOffset",
        "BounceLaser"
      ]
    },
    {
      "method_id": "m025",
      "summary": "缓存的激光终点向量，避免重复计算。",
      "use_cases": [
        "快速获取终点",
        "减少性能开销"
      ],
      "key_methods": [
        "EndPoint",
        "GetEndPoint",
        "CalculateEndPoint"
      ]
    },
    {
      "method_id": "m026",
      "summary": "标记激光是否处于第一次更新状态。",
      "use_cases": [
        "初始化特定行为",
        "防止重复触发"
      ],
      "key_methods": [
        "FirstUpdate",
        "SetTimeout"
      ]
    },
    {
      "method_id": "m027",
      "summary": "指示激光在当前帧是否被网格实体阻挡。",
      "use_cases": [
        "环境碰撞检测",
        "决定激光是否终止"
      ],
      "key_methods": [
        "GridHit",
        "CalculateEndPoint"
      ]
    },
    {
      "method_id": "m028",
      "summary": "与追踪相关的内部数据。",
      "use_cases": [
        "高级追踪逻辑定制"
      ],
      "key_methods": [
        "HomingLaser",
        "SetHomingType",
        "HomingType"
      ]
    },
    {
      "method_id": "m029",
      "summary": "当前激光的追踪类型枚举值。",
      "use_cases": [
        "判断追踪模式",
        "读取追踪设置"
      ],
      "key_methods": [
        "HomingType",
        "SetHomingType",
        "HomingLaser"
      ]
    },
    {
      "method_id": "m030",
      "summary": "激光是否正在进行主动旋转。",
      "use_cases": [
        "检查旋转状态",
        "控制逻辑分支"
      ],
      "key_methods": [
        "IsActiveRotating",
        "SetActiveRotation"
      ]
    },
    {
      "method_id": "m031",
      "summary": "激光的实际长度。",
      "use_cases": [
        "获取或调整激光长度",
        "与最大距离对比"
      ],
      "key_methods": [
        "LaserLength",
        "SetMaxDistance",
        "MaxDistance"
      ]
    },
    {
      "method_id": "m032",
      "summary": "上一帧的角度（度），用于计算角度变化。",
      "use_cases": [
        "跟踪旋转增量",
        "防抖处理"
      ],
      "key_methods": [
        "LastAngleDegrees",
        "AngleDegrees",
        "SetActiveRotation"
      ]
    },
    {
      "method_id": "m033",
      "summary": "激光的最大延伸距离，0 表示无限制。",
      "use_cases": [
        "限制硫磺火射程",
        "动态调整距离"
      ],
      "key_methods": [
        "MaxDistance",
        "SetMaxDistance",
        "LaserLength"
      ]
    },
    {
      "method_id": "m034",
      "summary": "激光是否只命中一次。",
      "use_cases": [
        "设计一次性效果",
        "避免多重伤害"
      ],
      "key_methods": [
        "OneHit",
        "SetOneHit"
      ]
    },
    {
      "method_id": "m035",
      "summary": "相对于父实体的偏移向量。",
      "use_cases": [
        "设定子激光位置",
        "跟随父实体"
      ],
      "key_methods": [
        "ParentOffset",
        "DisableFollowParent",
        "BounceLaser"
      ]
    },
    {
      "method_id": "m036",
      "summary": "激光的碰撞半径。",
      "use_cases": [
        "调整激光粗细",
        "修改碰撞检测范围"
      ],
      "key_methods": [
        "Radius"
      ]
    },
    {
      "method_id": "m037",
      "summary": "当前旋转角度（度）。",
      "use_cases": [
        "读取或修改旋转角度",
        "生成旋转动画"
      ],
      "key_methods": [
        "RotationDegrees",
        "SetActiveRotation",
        "RotationSpd"
      ]
    },
    {
      "method_id": "m038",
      "summary": "旋转开始前的延迟帧数。",
      "use_cases": [
        "控制旋转启动时间",
        "实现延迟旋转效果"
      ],
      "key_methods": [
        "RotationDelay",
        "SetActiveRotation"
      ]
    },
    {
      "method_id": "m039",
      "summary": "旋转速度。",
      "use_cases": [
        "调整旋转快慢",
        "设置动态旋转"
      ],
      "key_methods": [
        "RotationSpd",
        "SetActiveRotation",
        "RotationDegrees"
      ]
    },
    {
      "method_id": "m040",
      "summary": "标识是否为采样渲染模式激光。",
      "use_cases": [
        "判断渲染方式",
        "优化绘制"
      ],
      "key_methods": [
        "SampleLaser",
        "IsSampleLaser"
      ]
    },
    {
      "method_id": "m041",
      "summary": "激光是否正在收缩消失。",
      "use_cases": [
        "检测生命周期末期",
        "播放收缩特效"
      ],
      "key_methods": [
        "Shrink"
      ]
    },
    {
      "method_id": "m042",
      "summary": "旋转起始角度，用于随机旋转的起始参考。",
      "use_cases": [
        "记录起始角度",
        "计算旋转偏移"
      ],
      "key_methods": [
        "StartAngleDegrees",
        "SetActiveRotation"
      ]
    },
    {
      "method_id": "m043",
      "summary": "激光当前的泪弹标志集合。",
      "use_cases": [
        "读取或覆盖完整泪弹标志",
        "调试激光属性"
      ],
      "key_methods": [
        "TearFlags",
        "AddTearFlags",
        "ClearTearFlags",
        "HasTearFlags"
      ]
    },
    {
      "method_id": "m044",
      "summary": "激光剩余存活帧数。",
      "use_cases": [
        "获取剩余时间",
        "控制消失时机"
      ],
      "key_methods": [
        "Timeout",
        "SetTimeout"
      ]
    }
  ]
}
```
