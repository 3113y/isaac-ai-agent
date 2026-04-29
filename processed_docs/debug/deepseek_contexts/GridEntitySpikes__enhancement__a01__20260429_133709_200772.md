# DeepSeek Context

- class: GridEntitySpikes
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:37:09.200806

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

类名：GridEntitySpikes

原始 md 文档（该类完整文档，可能已截断）：
# Class "GridEntitySpikes"

???+ info
    You can get this class by using the following function:

    * [GridEntity.ToSpikes()](GridEntity.md#tospikes)

    ???+ example "Example Code"
        `Game():GetRoom():GetGridEntity(25):ToSpikes()`

## Class Diagram
--8<-- "docs/snippets/GridEntityClassDiagram.md"
## Variables
### Timeout {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Timeout  {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
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
    "summary": "GridEntitySpikes 代表游戏中的可伸缩尖刺网格实体，通过 Timeout 变量控制尖刺的伸出与收回状态切换。",
    "use_cases": [
      "创建自定义行为的伸缩尖刺",
      "读取或修改尖刺状态计时以实现特殊房间机制"
    ],
    "key_methods": [
      "Timeout"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "控制尖刺伸出/收回状态切换的整数计时器，每次状态切换后重置倒计时，当值为 0 时触发下一次状态变化。",
      "use_cases": [
        "延长或缩短尖刺伸出/收回的间隔时间",
        "同步尖刺状态与其他实体行为"
      ],
      "key_methods": [
        "Timeout"
      ]
    }
  ]
}
```
