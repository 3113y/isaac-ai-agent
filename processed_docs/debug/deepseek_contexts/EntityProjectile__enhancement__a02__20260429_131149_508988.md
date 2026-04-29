# DeepSeek Context

- class: EntityProjectile
- stage: enhancement
- attempt: 2
- model: deepseek-v4-pro
- max_tokens: 3400
- temperature: 0
- timestamp: 2026-04-29T13:11:49.509090

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

类名：EntityProjectile

原始 md 文档（该类完整文档，可能已截断）：
# Class "EntityProjectile"

???+ info
    You can get this class by using the following function:

    * [Entity.ToProjectile()](Entity.md#toprojectile)
    * [EntityNPC.FireBossProjectiles()](EntityNPC.md#firebossprojectiles)

    ???+ example "Example Code"
        `local entity = Isaac.GetRoomEntities()[1]:ToProjectile()`

## Class Diagram
--8<-- "docs/snippets/EntityClassDiagram.md"
## Functions
### Add·Change·Flags () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddChangeFlags ( [ProjectileFlags](enums/ProjectileFlags.md) Flags ) {: .copyable aria-label='Functions' }

See [ChangeFlags](#changeflags).
___
### Add·Falling·Accel () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddFallingAccel ( float Value ) {: .copyable aria-label='Functions' }

___
### Add·Falling·Speed () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddFallingSpeed ( float Value ) {: .copyable aria-label='Functions' }

___
### Add·Height () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddHeight ( float Value ) {: .copyable aria-label='Functions' }

___
### Add·Projectile·Flags () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddProjectileFlags ( [ProjectileFlags](enums/ProjectileFlags.md) Flags ) {: .copyable aria-label='Functions' }

You can change the attributes of the projectile by adding one or more [`ProjectileFlag`](enums/ProjectileFlags.md).

___
### Add·Scale () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddScale ( float Value ) {: .copyable aria-label='Functions' }

___
### Clear·Projectile·Flags () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void ClearProjectileFlags ( [ProjectileFlags](enums/ProjectileFlags.md) Flags ) {: .copyable aria-label='Functions' }

___
### Has·Projectile·Flags () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean HasProjectileFlags ( [ProjectileFlags](enums/ProjectileFlags.md) Flags ) {: .copyable aria-label='Functions' }

___
## Variables
### Acceleration {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Acceleration  {: .copyable aria-label='Variables' }

___
### Change·Flags {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [ProjectileFlags](enums/ProjectileFlags.md) ChangeFlags  {: .copyable aria-label='Variables' }

Uses [ProjectileFlags](enums/ProjectileFlags.md) to define the projectile attributes after the "Changed" state was activated.
The [ProjectileFlag](enums/ProjectileFlags.md).CHANGE_FLAGS_AFTER_TIMEOUT needs to be set to allow for this change to apply!
____
**Informations about "Changed" State:**

Projectiles can have two states: normal (default) and changed.


Changed state activates when projectile's frame count reaches the value set in [ChangeTimeout](#changetimeout). After that its flags get changed to what was set in [ChangeFlags](#changeflags) and velocity will be resized to length set in [ChangeVelocity](#changevelocity).
____
Also used in: [ProjectileParams()](ProjectileParams.md)
___
### Change·Timeout {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ChangeTimeout  {: .copyable aria-label='Variables' }

Number of frames that need to elapse after spawn till the "Changed" state is activated.
The [ProjectileFlags](enums/ProjectileFlags.md).CHANGE_FLAGS_AFTER_TIMEOUT or CHANGE_VELOCITY_AFTER_TIMEOUT need to be set to allow for this change to apply!
____
**Informations about "Changed" State:**

Projectiles can have two states: normal (default) and changed.


Changed state activates when projectile's frame count reaches the value set in [ChangeTimeout](#changetimeout). After that its flags get changed to what was set in [ChangeFlags](#changeflags) and velocity will be resized to length set in [ChangeVelocity](#changevelocity).
____
Also used in: [ProjectileParams()](ProjectileParams.md)
___
### Change·Velocity {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float ChangeVelocity  {: .copyable aria-label='Variables' }

Velocity value that gets applied when the "Changed" state is activated.
The [ProjectileFlag](enums/ProjectileFlags.md).CHANGE_VELOCITY_AFTER_TIMEOUT need to be set to allow for this change to apply!
____
**Informations about "Changed" State:**

Projectiles can have two states: normal (default) and changed.


Changed state activates when projectile's frame count reaches the value set in [ChangeTimeout](#changetimeout). After that its flags get changed to what was set in [ChangeFlags](#changeflags) and velocity will be resized to length set in [ChangeVelocity](#changevelocity).
____
Also used in: [ProjectileParams()](ProjectileParams.md)
___
### Curving·Strength {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float CurvingStrength  {: .copyable aria-label='Variables' }

___
### Damage {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Damage  {: .copyable aria-label='Variables' }

___
### Depth·Offset {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float DepthOffset  {: .copyable aria-label='Variables' }

___
### Falling·Accel {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float FallingAccel  {: .copyable aria-label='Variables' }

___
### Falling·Speed {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float FallingSpeed  {: .copyable aria-label='Variables' }

___
### Height {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Height  {: .copyable aria-label='Variables' }

Defines the height of a projectile. Height should be a negative value. Default is `:::lua -23`.
To make projectiles that remain at a perfectly stationary Height until collision, set FallingSpeed to `:::lua 0` and FallingAccel to `:::lua -0.1`.
___
### Homing·Strength {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float HomingStrength  {: .copyable aria-label='Variables' }

___
### Projectile·Flags {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [ProjectileFlags](enums/ProjectileFlags.md) ProjectileFlags {: .copyable aria-label='Variables' }

Uses [ProjectileFlags](enums/ProjectileFlags.md) to define the projectile attributes.
___
### Scale {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Scale  {: .copyable aria-label='Variables' }

___
### Wiggle·Frame·Offset {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int WiggleFrameOffset  {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "AddChangeFlags",
    "signature": "void AddChangeFlags ( [ProjectileFlags](enums/ProjectileFlags.md) Flags ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "AddFallingAccel",
    "signature": "void AddFallingAccel ( float Value ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "AddFallingSpeed",
    "signature": "void AddFallingSpeed ( float Value ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "AddHeight",
    "signature": "void AddHeight ( float Value ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "AddProjectileFlags",
    "signature": "void AddProjectileFlags ( [ProjectileFlags](enums/ProjectileFlags.md) Flags ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "AddScale",
    "signature": "void AddScale ( float Value ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "ClearProjectileFlags",
    "signature": "void ClearProjectileFlags ( [ProjectileFlags](enums/ProjectileFlags.md) Flags ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "HasProjectileFlags",
    "signature": "boolean HasProjectileFlags ( [ProjectileFlags](enums/ProjectileFlags.md) Flags ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "Acceleration",
    "signature": "float Acceleration  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "ChangeFlags",
    "signature": "[ProjectileFlags](enums/ProjectileFlags.md) ChangeFlags  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "ChangeTimeout",
    "signature": "int ChangeTimeout  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "ChangeVelocity",
    "signature": "float ChangeVelocity  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "CurvingStrength",
    "signature": "float CurvingStrength  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "Damage",
    "signature": "float Damage  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "DepthOffset",
    "signature": "float DepthOffset  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m016",
    "name": "FallingAccel",
    "signature": "float FallingAccel  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m017",
    "name": "FallingSpeed",
    "signature": "float FallingSpeed  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m018",
    "name": "Height",
    "signature": "float Height  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m019",
    "name": "HomingStrength",
    "signature": "float HomingStrength  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m020",
    "name": "ProjectileFlags",
    "signature": "[ProjectileFlags](enums/ProjectileFlags.md) ProjectileFlags {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m021",
    "name": "Scale",
    "signature": "float Scale  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m022",
    "name": "WiggleFrameOffset",
    "signature": "int WiggleFrameOffset  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "表示游戏中的投射物实体，提供属性与标志的动态修改，支持超时触发状态切换。",
    "use_cases": ["自定义投射物轨迹与行为", "创建定时改变属性的子弹"],
    "key_methods": ["AddProjectileFlags", "ChangeFlags", "HasProjectileFlags"]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "向ChangeFlags添加标志，定义超时后切换的状态属性。",
      "use_cases": ["设置改变后的弹幕特性", "动态组合多个标志"],
      "key_methods": ["AddChangeFlags", "ChangeFlags", "ChangeTimeout"]
    },
    {
      "method_id": "m002",
      "summary": "增加投射物的下落加速度，影响高度变化。",
      "use_cases": ["调整抛物线轨迹", "重力效果微调"],
      "key_methods": ["AddFallingAccel", "FallingAccel", "AddFallingSpeed"]
    },
    {
      "method_id": "m003",
      "summary": "增加投射物的下落速度，改变垂直移动快慢。",
      "use_cases": ["控制坠落节奏", "修正垂直偏移"],
      "key_methods": ["AddFallingSpeed", "FallingSpeed", "AddFallingAccel"]
    },
    {
      "method_id": "m004",
      "summary": "增加投射物的当前高度值。",
      "use_cases": ["模拟跳跃上升", "调整垂直打击点"],
      "key_methods": ["AddHeight", "Height", "FallingSpeed"]
    },
    {
      "method_id": "m005",
      "summary": "添加ProjectileFlags标志，赋予或叠加行为属性。",
      "use_cases": ["动态赋予追踪或穿透", "组合标志实现复杂子弹"],
      "key_methods": ["AddProjectileFlags", "ProjectileFlags", "ClearProjectileFlags"]
    },
    {
      "method_id": "m006",
      "summary": "增加投射物的视觉缩放比例。",
      "use_cases": ["尺寸渐变效果", "视觉比例调整"],
      "key_methods": ["AddScale", "Scale"]
    },
    {
      "method_id": "m007",
      "summary": "清除指定的ProjectileFlags标志。",
      "use_cases": ["移除临时特性", "重置默认行为"],
      "key_methods": ["ClearProjectileFlags", "ProjectileFlags", "AddProjectileFlags"]
    },
    {
      "method_id": "m008",
      "summary": "检查投射物是否拥有指定标志。",
      "use_cases": ["条件判断分支", "根据标志触发效果"],
      "key_methods": ["HasProjectileFlags", "ProjectileFlags", "AddProjectileFlags"]
    },
    {
      "method_id": "m009",
      "summary": "投射物的加速度值，影响速度随时间变化。",
      "use_cases": ["实现逐渐加速", "设置恒定变速"],
      "key_methods": ["Acceleration"]
    },
    {
      "method_id": "m010",
      "summary": "超时后切换的标志集，定义改变后的属性。",
      "use_cases": ["预置改变状态", "配合ChangeTimeout切换模式"],
      "key_methods": ["ChangeFlags", "AddChangeFlags", "ChangeTimeout"]
    },
    {
      "method_id": "m011",
      "summary": "从生成到状态改变所需的帧数。",
      "use_cases": ["延迟弹幕变形", "定时切换轨迹"],
      "key_methods": ["ChangeTimeout", "ChangeFlags", "ChangeVelocity"]
    },
    {
      "method_id": "m012",
      "summary": "状态改变后应用的速度大小。",
      "use_cases": ["改变后弹幕加速", "统一化速度向量长度"],
      "key_methods": ["ChangeVelocity", "ChangeTimeout", "ChangeFlags"]
    },
    {
      "method_id": "m013",
      "summary": "曲线运动强度，影响弹道弯曲程度。",
      "use_cases": ["实现弧形飞行", "调整追踪前摇"],
      "key_methods": ["CurvingStrength"]
    },
    {
      "method_id": "m014",
      "summary": "投射物造成的伤害数值。",
      "use_cases": ["设置威胁等级", "平衡弹幕威力"],
      "key_methods": ["Damage"]
    },
    {
      "method_id": "m015",
      "summary": "深度偏移，控制渲染层级。",
      "use_cases": ["调整视觉前后顺序", "伪3D效果"],
      "key_methods": ["DepthOffset"]
    },
    {
      "method_id": "m016",
      "summary": "下落加速度变量，定义重力效果强度。",
      "use_cases": ["创造不同重力环境", "控制高度变化率"],
      "key_methods": ["FallingAccel", "AddFallingAccel", "FallingSpeed"]
    },
    {
      "method_id": "m017",
      "summary": "下落速度变量，影响垂直移动速度。",
      "use_cases": ["设定初始下落快慢", "维持恒定坠落"],
      "key_methods": ["FallingSpeed", "AddFallingSpeed", "FallingAccel"]
    },
    {
      "method_id": "m018",
      "summary": "投射物当前高度，通常为负值。",
      "use_cases": ["判断地面碰撞", "实现跳跃动画"],
      "key_methods": ["Height", "AddHeight", "FallingSpeed"]
    },
    {
      "method_id": "m019",
      "summary": "追踪强度，控制向目标变向的程度。",
      "use_cases": ["制作制导子弹", "调整追踪灵敏度"],
      "key_methods": ["HomingStrength"]
    },
    {
      "method_id": "m020",
      "summary": "投射物的行为标志变量，可读写。",
      "use_cases": ["读取当前标志状态", "整体替换标志集"],
      "key_methods": ["ProjectileFlags", "AddProjectileFlags", "HasProjectileFlags"]
    },
    {
      "method_id": "m021",
      "summary": "投射物的视觉缩放比例变量。",
      "use_cases": ["动态改变大小", "统一缩放引用"],
      "key_methods": ["Scale", "AddScale"]
    },
    {
      "method_id": "m022",
      "summary": "摆动动画的起始帧偏移量。",
      "use_cases": ["同步摆动相位", "创造错落摆动效果"],
      "key_methods": ["WiggleFrameOffset"]
    }
  ]
}
```
