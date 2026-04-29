# DeepSeek Context

- class: EntityEffect
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T12:50:24.467429

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

类名：EntityEffect

原始 md 文档（该类完整文档，可能已截断）：
# Class "EntityEffect"

???+ info
    You can get this class by using the following function:

    * [Entity.ToEffect()](Entity.md#toeffect)
    * [EntityNPC.MakeSplat()](EntityNPC.md#makesplat)

    ???+ example "Example Code"
        `local entity = Isaac.GetRoomEntities()[1]:ToEffect()`

## Class Diagram
--8<-- "docs/snippets/EntityClassDiagram.md"
## Functions
### Follow·Parent () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void FollowParent ( [Entity](Entity.md) Parent ) {: .copyable aria-label='Functions' }

___
### Is·Player·Creep () {: aria-label='Functions' }
[ ](#){: .static .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### static boolean IsPlayerCreep ( [EffectVariant](enums/EffectVariant.md) Variant ) {: .copyable aria-label='Functions' }

___
### Set·Damage·Source () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetDamageSource ( [EntityType](enums/EntityType.md) DamageSource ) {: .copyable aria-label='Functions' }

___
### Set·Radii () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetRadii ( float min, float max ) {: .copyable aria-label='Functions' }
用于冲击波（shockwaves）。
___
### Set·Timeout () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetTimeout ( int Timeout ) {: .copyable aria-label='Functions' }

___
## Variables
### Damage·Source {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int DamageSource  {: .copyable aria-label='Variables' }

___
### Falling·Acceleration {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float FallingAcceleration  {: .copyable aria-label='Variables' }

___
### Falling·Speed {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float FallingSpeed  {: .copyable aria-label='Variables' }

___
### Is·Following {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsFollowing  {: .copyable aria-label='Variables' }

___
### Life·Span {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int LifeSpan  {: .copyable aria-label='Variables' }

___
### m_Height {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float m_Height  {: .copyable aria-label='Variables' }
用于粒子的 .dy

___
### Max·Radius {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float MaxRadius  {: .copyable aria-label='Variables' }

___
### Min·Radius {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float MinRadius  {: .copyable aria-label='Variables' }
用于冲击波（shockwaves）。

___
### Parent·Offset {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) ParentOffset  {: .copyable aria-label='Variables' }
可能很快就会被淘汰，取而代之的是 m_SpriteOffset

___
### Rotation {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Rotation  {: .copyable aria-label='Variables' }

___
### Scale {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Scale  {: .copyable aria-label='Variables' }

___
### State {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int State  {: .copyable aria-label='Variables' }
状态变量，可在 Init() 中随意使用，初始化为 0

___
### Timeout {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Timeout  {: .copyable aria-label='Variables' }

该值在每一帧都会递减，即使是自定义效果也是如此。自定义效果将此值初始化为 -1。

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "FollowParent",
    "signature": "void FollowParent ( [Entity](Entity.md) Parent ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "IsPlayerCreep",
    "signature": "static boolean IsPlayerCreep ( [EffectVariant](enums/EffectVariant.md) Variant ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "SetDamageSource",
    "signature": "void SetDamageSource ( [EntityType](enums/EntityType.md) DamageSource ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "SetRadii",
    "signature": "void SetRadii ( float min, float max ) {: .copyable aria-label='Functions' }",
    "description": "用于冲击波（shockwaves）。"
  },
  {
    "method_id": "m005",
    "name": "SetTimeout",
    "signature": "void SetTimeout ( int Timeout ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "DamageSource",
    "signature": "int DamageSource  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "FallingAcceleration",
    "signature": "float FallingAcceleration  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "FallingSpeed",
    "signature": "float FallingSpeed  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "IsFollowing",
    "signature": "boolean IsFollowing  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "LifeSpan",
    "signature": "int LifeSpan  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "m_Height",
    "signature": "float m_Height  {: .copyable aria-label='Variables' }",
    "description": "用于粒子的 .dy"
  },
  {
    "method_id": "m012",
    "name": "MaxRadius",
    "signature": "float MaxRadius  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "MinRadius",
    "signature": "float MinRadius  {: .copyable aria-label='Variables' }",
    "description": "用于冲击波（shockwaves）。"
  },
  {
    "method_id": "m014",
    "name": "ParentOffset",
    "signature": "[Vector](Vector.md) ParentOffset  {: .copyable aria-label='Variables' }",
    "description": "可能很快就会被淘汰，取而代之的是 m_SpriteOffset"
  },
  {
    "method_id": "m015",
    "name": "Rotation",
    "signature": "float Rotation  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m016",
    "name": "Scale",
    "signature": "float Scale  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m017",
    "name": "State",
    "signature": "int State  {: .copyable aria-label='Variables' }",
    "description": "状态变量，可在 Init() 中随意使用，初始化为 0"
  },
  {
    "method_id": "m018",
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
    "summary": "EntityEffect 是用于表示游戏中各种视觉特效的实体类，如冲击波、水迹、粒子等。提供跟随父实体、设置伤害来源、配置半径、控制持续时间和下落物理效果等功能。",
    "use_cases": [
      "制作自定义冲击波特效",
      "实现粒子跟随玩家",
      "创建掉落物效果",
      "判断玩家毒液",
      "管理特效生命周期"
    ],
    "key_methods": [
      "SetTimeout",
      "SetRadii",
      "FollowParent",
      "IsPlayerCreep",
      "SetDamageSource"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "使当前特效跟随指定的父实体，让效果附着在目标上移动。",
      "use_cases": [
        "让粒子环绕玩家",
        "将特效粘附在怪物上"
      ],
      "key_methods": [
        "FollowParent",
        "IsFollowing",
        "ParentOffset"
      ]
    },
    {
      "method_id": "m002",
      "summary": "静态方法，检查给定的 EffectVariant 是否属于玩家留下的毒液（如妈踩后产生的液体）。",
      "use_cases": [
        "判断地面液体是否为玩家来源",
        "伤害结算时区分归属"
      ],
      "key_methods": [
        "IsPlayerCreep"
      ]
    },
    {
      "method_id": "m003",
      "summary": "设置该特效造成的伤害来源实体类型，用于归属判定。",
      "use_cases": [
        "让爆炸伤害统计为玩家",
        "标明环境伤害来源"
      ],
      "key_methods": [
        "SetDamageSource",
        "DamageSource"
      ]
    },
    {
      "method_id": "m004",
      "summary": "设置冲击波的内外半径，控制其影响范围。",
      "use_cases": [
        "动态调整爆炸冲击波大小",
        "制作扩散环效果"
      ],
      "key_methods": [
        "SetRadii",
        "MinRadius",
        "MaxRadius"
      ]
    },
    {
      "method_id": "m005",
      "summary": "设置特效的自动消失倒计时帧数。",
      "use_cases": [
        "控制粒子存在时长",
        "让临时特效到时自动清除"
      ],
      "key_methods": [
        "SetTimeout",
        "Timeout"
      ]
    },
    {
      "method_id": "m006",
      "summary": "整数属性，存储该特效的伤害来源实体类型。",
      "use_cases": [
        "读取伤害来源做统计",
        "修改已存在的伤害归属"
      ],
      "key_methods": [
        "DamageSource",
        "SetDamageSource"
      ]
    },
    {
      "method_id": "m007",
      "summary": "下落加速度，模拟重力影响，用于掉落类特效。",
      "use_cases": [
        "实现陨石加速坠落",
        "制作越落越快的粒子"
      ],
      "key_methods": [
        "FallingAcceleration",
        "FallingSpeed"
      ]
    },
    {
      "method_id": "m008",
      "summary": "当前下落速度，与 FallingAcceleration 配合使用。",
      "use_cases": [
        "读取当前坠落速度以调整动画",
        "让掉落物弹跳"
      ],
      "key_methods": [
        "FallingSpeed",
        "FallingAcceleration"
      ]
    },
    {
      "method_id": "m009",
      "summary": "布尔值，指示该特效当前是否正在跟随父实体。",
      "use_cases": [
        "判断跟随状态以切换行为",
        "解绑跟随前检查"
      ],
      "key_methods": [
        "IsFollowing",
        "FollowParent"
      ]
    },
    {
      "method_id": "m010",
      "summary": "特效的总生命帧数，控制其最大存在时长。",
      "use_cases": [
        "设置长粒子存在时间",
        "获取剩余寿命比例"
      ],
      "key_methods": [
        "LifeSpan",
        "Timeout"
      ]
    },
    {
      "method_id": "m011",
      "summary": "特效高度值，直接影响渲染时粒子的 .dy 偏移，用于表现层次感。",
      "use_cases": [
        "制作漂浮粒子效果",
        "实现立体感冲击波"
      ],
      "key_methods": [
        "m_Height"
      ]
    },
    {
      "method_id": "m012",
      "summary": "冲击波的最大半径，与 SetRadii 配合控制外边界。",
      "use_cases": [
        "读取冲击波当前最大范围",
        "动态缩放冲击波大小"
      ],
      "key_methods": [
        "MaxRadius",
        "SetRadii"
      ]
    },
    {
      "method_id": "m013",
      "summary": "冲击波的最小半径，与 MaxRadius 一起定义中空区域。",
      "use_cases": [
        "制作中空冲击波",
        "读取内径进行精确碰撞"
      ],
      "key_methods": [
        "MinRadius",
        "SetRadii"
      ]
    },
    {
      "method_id": "m014",
      "summary": "特效相对于跟随父实体的偏移向量，即将被 m_S
```
