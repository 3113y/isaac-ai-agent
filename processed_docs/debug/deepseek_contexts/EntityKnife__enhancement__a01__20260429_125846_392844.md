# DeepSeek Context

- class: EntityKnife
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T12:58:46.392887

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

类名：EntityKnife

原始 md 文档（该类完整文档，可能已截断）：
# Class "EntityKnife"

???+ info
    You can get this class by using the following function:

    * [Entity.ToKnife()](Entity.md#toknife)
    * [EntityPlayer.FireKnife()](EntityPlayer.md#fireknife)

    ???+ example "Example Code"
        `local knifeEntity = Isaac.GetPlayer():FireKnife(Isaac.GetPlayer())`

## Class Diagram
--8<-- "docs/snippets/EntityClassDiagram.md"
## Functions
### Add·Tear·Flags () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }

___
### Clear·Tear·Flags () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void ClearTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }

___
### Get·Knife·Distance () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### float GetKnifeDistance ( ) {: .copyable aria-label='Functions' }

___
### Get·Knife·Velocity () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### float GetKnifeVelocity ( ) {: .copyable aria-label='Functions' }

___
### Get·Render·Z () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### int GetRenderZ ( ) {: .copyable aria-label='Functions' }

___
### Has·Tear·Flags () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean HasTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }

___
### Is·Flying () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsFlying ( ) {: .copyable aria-label='Functions' }

___
### Reset () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void Reset ( ) {: .copyable aria-label='Functions' }
用于主刀（master knifes），以使其返回到玩家。
___
### Set·Path·Follow·Speed () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetPathFollowSpeed ( float Speed ) {: .copyable aria-label='Functions' }

___
### Shoot () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void Shoot ( float Charge, float Range ) {: .copyable aria-label='Functions' }

___
## Variables
### Charge {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Charge  {: .copyable aria-label='Variables' }

___
### Max·Distance {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float MaxDistance  {: .copyable aria-label='Variables' }

___
### Path·Follow·Speed {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float PathFollowSpeed  {: .copyable aria-label='Variables' }
Unit speed of path moving knifes.
___
### Path·Offset {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float PathOffset  {: .copyable aria-label='Variables' }

___
### Rotation {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Rotation  {: .copyable aria-label='Variables' }

___
### Rotation·Offset {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float RotationOffset  {: .copyable aria-label='Variables' }

___
### Scale {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### float Scale  {: .copyable aria-label='Variables' }

___
### Tear·Flags {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [TearFlags](enums/TearFlags.md) TearFlags  {: .copyable aria-label='Variables' }

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
    "name": "ClearTearFlags",
    "signature": "void ClearTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "GetKnifeDistance",
    "signature": "float GetKnifeDistance ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "GetKnifeVelocity",
    "signature": "float GetKnifeVelocity ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "GetRenderZ",
    "signature": "int GetRenderZ ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "HasTearFlags",
    "signature": "boolean HasTearFlags ( [TearFlags](enums/TearFlags.md) Flags ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "IsFlying",
    "signature": "boolean IsFlying ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "Reset",
    "signature": "void Reset ( ) {: .copyable aria-label='Functions' }",
    "description": "用于主刀（master knifes），以使其返回到玩家。"
  },
  {
    "method_id": "m009",
    "name": "SetPathFollowSpeed",
    "signature": "void SetPathFollowSpeed ( float Speed ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "Shoot",
    "signature": "void Shoot ( float Charge, float Range ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "Charge",
    "signature": "float Charge  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "MaxDistance",
    "signature": "float MaxDistance  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "PathFollowSpeed",
    "signature": "float PathFollowSpeed  {: .copyable aria-label='Variables' }",
    "description": "Unit speed of path moving knifes."
  },
  {
    "method_id": "m014",
    "name": "PathOffset",
    "signature": "float PathOffset  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "Rotation",
    "signature": "float Rotation  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m016",
    "name": "RotationOffset",
    "signature": "float RotationOffset  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m017",
    "name": "Scale",
    "signature": "float Scale  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m018",
    "name": "TearFlags",
    "signature": "[TearFlags](enums/TearFlags.md) TearFlags  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "EntityKnife 代表一把飞刀实体，通常由玩家发射（如妈妈的刀）或作为路径跟随刀（如科技零）存在。提供控制刀的行为、泪液标志、运动参数和渲染属性的方法，用于自定义刀的飞行、返回和视觉表现。",
    "use_cases": [
      "动态修改刀的泪液效果（如添加追踪、穿透）",
      "获取刀的飞行距离与速度以实现碰撞或伤害逻辑",
      "控制主刀返回玩家身边",
      "调整路径刀的移动速度和偏移",
      "修改刀的渲染层级、旋转和缩放以定制外观"
    ],
    "key_methods": [
      "AddTearFlags",
      "Shoot",
      "Reset",
      "GetKnifeDistance",
      "SetPathFollowSpeed"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "为刀添加指定的泪液标志，从而赋予特殊效果（如穿透、追踪、爆炸等）。",
      "use_cases": [
        "制作有追踪效果的刀",
        "临时赋予穿透特性",
        "叠加多种泪液效果"
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
      "summary": "移除刀的特定泪液标志，取消对应效果。",
      "use_cases": [
        "某条件达成后移除追踪",
        "还原刀的基础行为",
        "状态切换时清理旧效果"
      ],
      "key_methods": [
        "ClearTearFlags",
        "AddTearFlags",
        "HasTearFlags"
      ]
    },
    {
      "method_id": "m003",
      "summary": "返回刀与发射者（或关联实体）之间的距离。",
      "use_cases": [
        "判断刀是否超出最大距离",
        "实现距离衰减伤害",
        "绘制环绕玩家视觉特效"
      ],
      "key_methods": [
        "GetKnifeDistance",
        "MaxDistance",
        "Shoot"
      ]
    },
    {
      "method_id": "m004",
      "summary": "获取刀的当前速度标量，用于运动计算或特效强度。",
      "use_cases": [
        "根据速度调整拖尾长度",
        "碰撞后速度重置",
        "伤害受速度影响"
      ],
      "key_methods": [
        "GetKnifeVelocity",
        "SetPathFollowSpeed",
        "GetKnifeDistance"
      ]
    },
    {
      "method_id": "m005",
      "summary": "获取刀在渲染顺序中的 Z 值，用于控制绘制层级。",
      "use_cases": [
        "确保刀渲染在玩家之上",
        "多层刀特效层级排序",
        "避免被其他实体遮挡"
      ],
      "key_methods": [
        "GetRenderZ",
        "Scale",
        "Rotation"
      ]
    },
    {
      "method_id": "m006",
      "summary": "检查刀是否拥有指定的泪液标志。",
      "use_cases": [
        "根据标志切换伤害类型",
        "条件性移除效果",
        "视觉反馈判定"
      ],
      "key_methods": [
        "HasTearFlags",
        "AddTearFlags",
        "ClearTearFlags",
        "TearFlags"
      ]
    },
    {
      "method_id": "m007",
      "summary": "返回刀是否处于飞行状态（无视障碍）。",
      "use_cases": [
        "决定刀的碰撞判定模式",
        "改变拖尾粒子效果",
        "逻辑区分飞行刀与地面刀"
      ],
      "key_methods": [
        "IsFlying",
        "GetKnifeVelocity",
        "AddTearFlags"
      ]
    },
    {
      "method_id": "m008",
      "summary": "使主刀强制返回玩家位置，常用于结束飞行或重置状态。",
      "use_cases": [
        "主动道具冷却时回收刀",
        "切换房间时重置位置",
        "强制停止远程攻击"
      ],
      "key_methods": [
        "Reset",
        "Shoot",
        "GetKnifeDistance"
      ]
    },
    {
      "method_id": "m009",
      "summary": "设置路径跟随刀沿路径移动的速度倍率。",
      "use_cases": [
        "调整科技零风格的环绕速度",
        "创建变速路径动画",
        "配合 PathOffset 动态移动"
      ],
      "key_methods": [
        "SetPathFollowSpeed",
        "PathFollowSpeed",
        "PathOffset"
      ]
    },
    {
      "method_id": "m010",
      "summary": "发射刀，由蓄力值和射程控制其飞行距离与速度。",
      "use_cases": [
        "制造可蓄力投掷的刀",
        "模拟妈妈的刀攻击",
        "自定义技能的射程计算"
      ],
      "key_methods": [
        "Shoot",
        "Charge",
        "MaxDistance",
        "Reset"
      ]
    },
    {
      "method_id": "m011",
      "summary": "刀的蓄力值，影响 Shoot 时的初始速度和/或射程。",
      "use_cases": [
        "组合蓄力条显示",
        "蓄力中断后重置为0",
        "满蓄力自动发射"
      ],
      "key_methods": [
        "Charge",
        "Shoot",
        "SetPathFollowSpeed"
      ]
    },
    {
      "method_id": "m012",
      "summary": "刀的最大飞行距离，超过后可能消失或返回。",
      "use_cases": [
        "自定义射程上限",
        "缩短或延长刀存活时间",
        "射程计数器"
      ],
      "key_methods": [
        "MaxDistance",
        "Shoot",
        "GetKnifeDistance"
      ]
    },
    {
      "method_id": "m013",
      "summary": "路径跟随刀的路径移动速度基础值，用于环绕或固定轨迹运动。",
      "use_cases": [
        "创建慢速护航刀",
        "调整科技零旋转速度",
        "与 PathOffset 配合实现动态螺旋"
      ],
      "key_methods": [
        "PathFollowSpeed",
        "SetPathFollowSpeed",
        "PathOffset"
      ]
    },
    {
      "method_id": "m014",
      "summary": "刀沿设定路径的偏移量，改变其在路径上的初始或当前位置。",
      "use_cases": [
        "多把刀均匀分布同一条路径",
        "创建波状运动",
        "动画循环偏移"
      ],
      "key_methods": [
        "PathOffset",
        "PathFollowSpeed",
        "SetPathFollowSpeed"
      ]
    },
    {
      "method_id": "m015",
      "summary": "刀的当前旋转角度（弧度或度），影响朝向和视觉效果。",
      "use_cases": [
        "随鼠标角度旋转刀",
        "生成扇形刀阵",
        "绘制旋转拖尾"
      ],
      "key_methods": [
        "Rotation",
        "RotationOffset",
        "Shoot"
      ]
    },
    {
      "method_id": "m016",
      "summary": "刀的基础旋转偏移量，叠加到 Rotation 上用于初始朝向。",
      "use_cases": [
        "固定多把刀均匀分布",
        "设置默认朝向",
        "在不改变逻辑角度下调整外观"
      ],
      "key_methods": [
        "RotationOffset",
        "Rotation",
        "Scale"
      ]
    },
    {
      "method_id": "m017",
      "summary": "刀的渲染缩放因子，改变视觉大小。",
      "use_cases": [
        "制作小刀变成大刀的成长效果",
        "蓄力时动态缩放",
        "统一调整多把刀的大小"
      ],
      "key_methods": [
        "Scale",
        "GetRenderZ",
        "Rotation"
      ]
    },
    {
      "method_id": "m018",
      "summary": "存储当前刀拥有的泪液标志组合，对应 Add/Clear/HasTearFlags。",
      "use_cases": [
        "直接读取当前全部标志",
        "用于条件判断或复制状态",
        "配合位运算组合新效果"
      ],
      "key_methods": [
        "TearFlags",
        "AddTearFlags",
        "ClearTearFlags",
        "HasTearFlags"
      ]
    }
  ]
}
```
