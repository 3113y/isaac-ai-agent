# DeepSeek Context

- class: EntityProjectile
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:08:35.367281

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
    "summary": "EntityProjectile 表示游戏中的投射物，用于控制和查询投射物的运动、状态标志、伤害、外观等属性，支持通过“changed”状态实现定时行为切换。",
    "use_cases": [
      "动态修改投射物属性以创建特殊弹幕",
      "实现投射物随时间改变行为（如加速、分裂）",
      "查询投射物当前状态以进行条件逻辑"
    ],
    "key_methods": [
      "AddProjectileFlags",
      "ChangeTimeout",
      "ChangeFlags",
      "ChangeVelocity",
      "HasProjectileFlags"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "添加一个或多个 ProjectileFlag 到 ChangeFlags 中，用于定义投射物进入 changed 状态后的标志。",
      "use_cases": [
        "预设投射物变化后的穿透/追踪等行为",
        "配合 ChangeTimeout 实现定时切换"
      ],
      "key_methods": [
        "AddChangeFlags",
        "ChangeFlags",
        "ChangeTimeout"
      ]
    },
    {
      "method_id": "m002",
      "summary": "按给定值增加投射物的下落加速度（FallingAccel），影响高度随时间变化的速率。",
      "use_cases": [
        "制作逐渐加速下落或抛射曲线",
        "实时调整下落运动"
      ],
      "key_methods": [
        "AddFallingAccel",
        "FallingAccel",
        "FallingSpeed",
        "Height"
      ]
    },
    {
      "method_id": "m003",
      "summary": "按给定值增加投射物的下落速度（FallingSpeed），直接影响高度下降快慢。",
      "use_cases": [
        "控制投射物落地速度",
        "配合 FallingAccel 实现物理效果"
      ],
      "key_methods": [
        "AddFallingSpeed",
        "FallingSpeed",
        "FallingAccel",
        "Height"
      ]
    },
    {
      "method_id": "m004",
      "summary": "按给定值增加投射物的高度，高度通常为负值，改变投射物的视觉效果位置。",
      "use_cases": [
        "调整投射物垂直位置",
        "实现跳跃或漂浮弹幕"
      ],
      "key_methods": [
        "AddHeight",
        "Height",
        "FallingSpeed",
        "FallingAccel"
      ]
    },
    {
      "method_id": "m005",
      "summary": "为投射物添加一个或多个 ProjectileFlag，用于启用例如追踪、穿透、燃烧等特殊行为。",
      "use_cases": [
        "动态赋予投射物新特性",
        "在特定条件触发时改变行为"
      ],
      "key_methods": [
        "AddProjectileFlags",
        "ProjectileFlags",
        "HasProjectileFlags",
        "ClearProjectileFlags"
      ]
    },
    {
      "method_id": "m006",
      "summary": "按给定值增加投射物的缩放比例（Scale），改变其视觉大小。",
      "use_cases": [
        "制作逐渐变大或缩小的弹幕",
        "根据距离调整视觉"
      ],
      "key_methods": [
        "AddScale",
        "Scale"
      ]
    },
    {
      "method_id": "m007",
      "summary": "清除投射物当前拥有的指定 ProjectileFlag，关闭对应的行为效果。",
      "use_cases": [
        "移除不再需要的特性（如追踪）",
        "实现状态切换"
      ],
      "key_methods": [
        "ClearProjectileFlags",
        "ProjectileFlags",
        "AddProjectileFlags",
        "HasProjectileFlags"
      ]
    },
    {
      "method_id": "m008",
      "summary": "检查投射物是否设有指定的 ProjectileFlag，返回布尔值。",
      "use_cases": [
        "条件判断投射物当前行为",
        "根据标志执行不同逻辑"
      ],
      "key_methods": [
        "HasProjectileFlags",
        "ProjectileFlags"
      ]
    },
    {
      "method_id": "m009",
      "summary": "浮点变量，表示投射物的加速度值，影响运动速度变化。",
      "use_cases": [
        "获取或设置投射物加速度",
        "配合曲率或追踪强度使用"
      ],
      "key_methods": [
        "Acceleration",
        "CurvingStrength",
        "HomingStrength"
      ]
    },
    {
      "method_id": "m010",
      "summary": "ProjectileFlags 变量，存储投射物进入 changed 状态后应用的标志组合。",
      "use_cases": [
        "定义变化后的投射物行为",
        "与 ChangeTimeout 共同作用"
      ],
      "key_methods": [
        "ChangeFlags",
        "ChangeTimeout",
        "ChangeVelocity",
        "AddChangeFlags"
      ]
    },
    {
      "method_id": "m011",
      "summary": "整型变量，设置从生成到激活 changed 状态所需的帧数。",
      "use_cases": [
        "控制投射物何时改变行为",
        "延时生效的特殊效果"
      ],
      "key_methods": [
        "ChangeTimeout",
        "ChangeFlags",
        "ChangeVelocity"
      ]
    },
    {
      "method_id": "m012",
      "summary": "浮点变量，指定 changed 状态激活后投射物的速度大小。",
      "use_cases": [
        "设置变化后的恒定速率",
        "配合标志变化实现新弹道"
      ],
      "key_methods": [
        "ChangeVelocity",
        "ChangeTimeout",
        "ChangeFlags"
      ]
    },
    {
      "method_id": "m013",
      "summary": "浮点变量，控制投射物曲线飞行的强度。",
      "use_cases": [
        "创建弧线或螺旋弹幕",
        "调整曲线行为的弯曲程度"
      ],
      "key_methods": [
        "CurvingStrength",
        "Acceleration"
      ]
    },
    {
      "method_id": "m014",
      "summary": "浮点变量
```
