# DeepSeek Context

- class: EntityLaser
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T12:59:55.988475

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

```
