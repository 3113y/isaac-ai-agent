# DeepSeek Context

- class: PlayerTypesPosVel
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T14:01:05.129950

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

类名：PlayerTypesPosVel

原始 md 文档（该类完整文档，可能已截断）：
# Class "PlayerTypesPosVel"

???+ info
    You can get this class by using the following function:

    * [EntityPlayer:GetMultiShotPositionVelocity()](EntityPlayer.md#getmultishotpositionvelocity)

## Variables
### Position {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) Position {: .copyable aria-label='Variables' }

___
### Velocity {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) Velocity {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "Position",
    "signature": "[Vector](Vector.md) Position {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "Velocity",
    "signature": "[Vector](Vector.md) Velocity {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "存储多方向射击时单个方向的位置和速度数据，由 EntityPlayer:GetMultiShotPositionVelocity() 返回。",
    "use_cases": [
      "自定义多方向子弹的发射逻辑",
      "基于位置与速度偏移生成特效或尾迹",
      "重写或扩展内置的多方向射击模式"
    ],
    "key_methods": [
      "Position",
      "Velocity"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "获取多方向射击中该方向对应的起始位置向量。",
      "use_cases": [
        "确定子弹生成点以进行自定义偏移",
        "根据位置生成射弹前的特效"
      ],
      "key_methods": [
        "Position",
        "Velocity"
      ]
    },
    {
      "method_id": "m002",
      "summary": "获取多方向射击中该方向对应的初始速度向量。",
      "use_cases": [
        "修改子弹的初始速度以实现弹幕效果",
        "基于速度值预测飞行路径或绘制指示线"
      ],
      "key_methods": [
        "Velocity",
        "Position"
      ]
    }
  ]
}
```
