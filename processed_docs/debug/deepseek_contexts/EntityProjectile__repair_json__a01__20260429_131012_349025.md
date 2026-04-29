# DeepSeek Context

- class: EntityProjectile
- stage: repair_json
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 3200
- temperature: 0
- timestamp: 2026-04-29T13:10:12.349244

## Prompt

```text
请把下面这段损坏的 JSON 文本修复为严格合法的 JSON。

要求：
1. 只输出 JSON 对象，不要任何解释。
2. 尽量保留原字段和语义，不要新增无关字段。
3. 顶层结构应为 {"class_enhancement": ..., "method_enhancements": ...}。
类名：EntityProjectile

损坏的 JSON：
{
  "class_enhancement": {
    "summary": "EntityProjectile 表示游戏中的投射物，用于控制和查询投射物的运动、状态标志、伤害、外观等属性，支持通过"changed"状态实现定时行为切换。",
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

## Response

```text
{
  "class_enhancement": {
    "summary": "EntityProjectile 表示游戏中的投射物，用于控制和查询投射物的运动、状态标志、伤害、外观等属性，支持通过\"changed\"状态实现定时行为切换。",
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
      "summary": "清除投射物当前拥有的指定 ProjectileFlag，关闭对应的
```
