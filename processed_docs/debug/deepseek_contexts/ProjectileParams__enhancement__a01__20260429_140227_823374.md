# DeepSeek Context

- class: ProjectileParams
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T14:02:27.823519

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

类名：ProjectileParams

原始 md 文档（该类完整文档，可能已截断）：
# Class "ProjectileParams"

???+ info
    This class can be accessed by using its constructor:

    ???+ example "Example Code"
        ```lua
        local myProjectileParams = ProjectileParams()
        ```

## Constructors
### Projectile·Params () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [ProjectileParams](ProjectileParams.md) ProjectileParams ( ) {: .copyable aria-label='Constructors' }

___
## Variables
### Acceleration {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Acceleration  {: .copyable aria-label='Variables' }

___
### Bullet·Flags {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int BulletFlags  {: .copyable aria-label='Variables' }

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
Also used in: [EntityProjectile](EntityProjectile.md)
___
### Change·Timeout {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ChangeTimeout  {: .copyable aria-label='Variables' }

Number of frames that need to elapse after spawn till the "Changed" state is activated.
The [ProjectileFlag](enums/ProjectileFlags.md).CHANGE_FLAGS_AFTER_TIMEOUT or CHANGE_VELOCITY_AFTER_TIMEOUT need to be set to allow for this change to apply!
____
**Informations about "Changed" State:**

Projectiles can have two states: normal (default) and changed.


Changed state activates when projectile's frame count reaches the value set in [ChangeTimeout](#changetimeout). After that its flags get changed to what was set in [ChangeFlags](#changeflags) and velocity will be resized to length set in [ChangeVelocity](#changevelocity).
____
Also used in: [EntityProjectile](EntityProjectile.md)
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
Also used in: [EntityProjectile](EntityProjectile.md)
___
### Circle·Angle {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float CircleAngle  {: .copyable aria-label='Variables' }
Angle offset used by fire_projectiles PROJECTILES_CIRCLE type emitter. Random by default.
___
### Color {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Color](Color.md) Color  {: .copyable aria-label='Variables' }

___
### Curving·Strength {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float CurvingStrength  {: .copyable aria-label='Variables' }
Use very small values for curving like 0.005.
___
### Depth·Offset {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float DepthOffset  {: .copyable aria-label='Variables' }

___
### Dot·Product·Limit {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float DotProductLimit  {: .copyable aria-label='Variables' }
Direction bullets are being fired in Dot product of FireDirectionLimit, bullet direction must be &gt;= this value
___
### Falling·Accel·Modifier {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float FallingAccelModifier  {: .copyable aria-label='Variables' }

___
### Falling·Speed·Modifier {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float FallingSpeedModifier  {: .copyable aria-label='Variables' }

___
### Fire·Direction·Limit {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) FireDirectionLimit  {: .copyable aria-label='Variables' }

___
### Grid·Collision {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean GridCollision  {: .copyable aria-label='Variables' }

___
### Height·Modifier {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float HeightModifier  {: .copyable aria-label='Variables' }

___
### Homing·Strength {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float HomingStrength  {: .copyable aria-label='Variables' }
Multiplier on normal homing strength. Unused if SMART bullet flag is not set.
___
### Position·Offset {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) PositionOffset  {: .copyable aria-label='Variables' }

___
### Scale {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Scale  {: .copyable aria-label='Variables' }

___
### Spread {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Spread  {: .copyable aria-label='Variables' }
For quad/quint/etc spread shots.
___
### Target·Position {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) TargetPosition  {: .copyable aria-label='Variables' }

___
### Variant {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Variant  {: .copyable aria-label='Variables' }

___
### Velocity·Multi {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float VelocityMulti  {: .copyable aria-label='Variables' }

___
### Wiggle·Frame·Offset {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int WiggleFrameOffset  {: .copyable aria-label='Variables' }
Used to offset the wiggle wave.
___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "ProjectileParams",
    "signature": "[ProjectileParams](ProjectileParams.md) ProjectileParams ( ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "Acceleration",
    "signature": "float Acceleration  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "BulletFlags",
    "signature": "int BulletFlags  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "ChangeFlags",
    "signature": "[ProjectileFlags](enums/ProjectileFlags.md) ChangeFlags  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "ChangeTimeout",
    "signature": "int ChangeTimeout  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "ChangeVelocity",
    "signature": "float ChangeVelocity  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "CircleAngle",
    "signature": "float CircleAngle  {: .copyable aria-label='Variables' }",
    "description": "Angle offset used by fire_projectiles PROJECTILES_CIRCLE type emitter. Random by default."
  },
  {
    "method_id": "m008",
    "name": "Color",
    "signature": "[Color](Color.md) Color  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "CurvingStrength",
    "signature": "float CurvingStrength  {: .copyable aria-label='Variables' }",
    "description": "Use very small values for curving like 0.005."
  },
  {
    "method_id": "m010",
    "name": "DepthOffset",
    "signature": "float DepthOffset  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "DotProductLimit",
    "signature": "float DotProductLimit  {: .copyable aria-label='Variables' }",
    "description": "Direction bullets are being fired in Dot product of FireDirectionLimit, bullet direction must be &gt;= this value"
  },
  {
    "method_id": "m012",
    "name": "FallingAccelModifier",
    "signature": "float FallingAccelModifier  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "FallingSpeedModifier",
    "signature": "float FallingSpeedModifier  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "FireDirectionLimit",
    "signature": "[Vector](Vector.md) FireDirectionLimit  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "GridCollision",
    "signature": "boolean GridCollision  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m016",
    "name": "HeightModifier",
    "signature": "float HeightModifier  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m017",
    "name": "HomingStrength",
    "signature": "float HomingStrength  {: .copyable aria-label='Variables' }",
    "description": "Multiplier on normal homing strength. Unused if SMART bullet flag is not set."
  },
  {
    "method_id": "m018",
    "name": "PositionOffset",
    "signature": "[Vector](Vector.md) PositionOffset  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m019",
    "name": "Scale",
    "signature": "float Scale  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m020",
    "name": "Spread",
    "signature": "float Spread  {: .copyable aria-label='Variables' }",
    "description": "For quad/quint/etc spread shots."
  },
  {
    "method_id": "m021",
    "name": "TargetPosition",
    "signature": "[Vector](Vector.md) TargetPosition  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m022",
    "name": "Variant",
    "signature": "int Variant  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m023",
    "name": "VelocityMulti",
    "signature": "float VelocityMulti  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m024",
    "name": "WiggleFrameOffset",
    "signature": "int WiggleFrameOffset  {: .copyable aria-label='Variables' }",
    "description": "Used to offset the wiggle wave."
  }
]

```

## Response

```text
{"class_enhancement": {"summary": "ProjectileParams 是一个参数容器类，用于在发射投射物时传递自定义属性，如速度、颜色、碰撞、变化状态及扩散角度等，配合 EntityPlayer:FireProjectile 等函数使用。", "use_cases": ["自定义玩家发射的子弹行为", "创建特殊敌人的弹幕模式", "实现延时形态变化的投射物", "配置多重射击的扩散与布局"], "key_methods": ["ProjectileParams", "ChangeFlags", "Spread", "BulletFlags", "HomingStrength"]}, "method_enhancements": [{"method_id": "m001", "summary": "构造 ProjectileParams 实例，用于存放投射物的各项自定义参数，可通过链式赋值后传递给发射函数。", "use_cases": ["创建空白参数对象以便按需设置属性", "结合 Game():SpawnEntity() 或 FireProjectile 发射自定义投射物"], "key_methods": ["ProjectileParams", "Variant", "Spread", "VelocityMulti", "Color"]}, {"method_id": "m002", "summary": "设置投射物的加速度值，影响其速度随时间的变化。", "use_cases": ["模拟重力或加速效果", "实现投射物速度曲线"], "key_methods": ["Acceleration", "FallingAccelModifier", "VelocityMulti"]}, {"method_id": "m003", "summary": "设置子弹的额外标志位（Bitmask），用于启用特定子弹行为（如穿透、跟踪等）。", "use_cases": ["让子弹获得穿透或磁性效果", "组合多种子弹特效"], "key_methods": ["BulletFlags", "ChangeFlags", "HomingStrength"]}, {"method_id": "m004", "summary": "指定投射物进入
```
