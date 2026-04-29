# DeepSeek Context

- class: GridEntityTNT
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:37:28.653120

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

类名：GridEntityTNT

原始 md 文档（该类完整文档，可能已截断）：
# Class "GridEntityTNT"

???+ info
    You can get this class by using the following function:

    * [GridEntity.ToTNT()](GridEntity.md#totnt)

    ???+ example "Example Code"
        `Game():GetRoom():GetGridEntity(25):ToTNT()`

## Class Diagram
--8<-- "docs/snippets/GridEntityClassDiagram.md"
## Variables
### Frame·Cnt {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int FrameCnt  {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "FrameCnt",
    "signature": "int FrameCnt  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "GridEntityTNT 代表可爆炸的 TNT 桶网格实体，通常通过 GridEntity.ToTNT() 获得，用于控制和检测 TNT 的状态。",
    "use_cases": [
      "检测 TNT 实体是否存在",
      "控制 TNT 爆炸或点燃",
      "读取或修改 TNT 的帧计数以影响动画/计时"
    ],
    "key_methods": [
      "FrameCnt"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "获取或设置 TNT 实体的帧计数器，用于控制爆炸前的动画进度或计时。",
      "use_cases": [
        "读取 TNT 剩余爆炸帧数",
        "修改帧计数以加快或延迟爆炸"
      ],
      "key_methods": [
        "FrameCnt"
      ]
    }
  ]
}
```
