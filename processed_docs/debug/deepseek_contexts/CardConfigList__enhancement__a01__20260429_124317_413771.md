# DeepSeek Context

- class: CardConfigList
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T12:43:17.413811

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

类名：CardConfigList

原始 md 文档（该类完整文档，可能已截断）：
# Class "CardConfigList"

???+ info
    You can get this class by using the following function:

    * [ItemConfig.GetCards()](ItemConfig.md#getcards)

    ???+ example "Example Code"
        `local cardConfigs = Isaac.GetItemConfig():GetCards()`

## Operators
### __len () {: aria-label='Operators' }
[ ](#){: .alldlc .tooltip .badge }
#### int __len ( ) {: .copyable aria-label='Operators' }

The length (#) operation. Returns the amount of cards in the list.

___
## Functions
### Get () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### userdata Get ( int idx ) {: .copyable aria-label='Functions' }

Returns userdata at the index of the list provided.

???+ bug "Bugs"
    This function does not return usable userdata, rendering it useless.

___
## Variables
### Size {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int Size  {: .copyable aria-label='Variables' }

The amount of cards in the list.

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "__len",
    "signature": "int __len ( ) {: .copyable aria-label='Operators' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "Get",
    "signature": "userdata Get ( int idx ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "Size",
    "signature": "const int Size  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "代表游戏中所有卡片配置的列表，通过 ItemConfig:GetCards() 获取，主要用于遍历和统计卡片数量。Get 方法由于 bug 暂时无法使用。",
    "use_cases": [
      "遍历所有卡片配置",
      "获取卡片总数",
      "使用 # 操作符或 Size 变量进行循环控制"
    ],
    "key_methods": [
      "Size",
      "__len",
      "Get"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "实现取长度运算符 #，返回列表中的卡片数量，与 Size 变量等效。",
      "use_cases": [
        "快速获取列表长度",
        "配合循环遍历卡片"
      ],
      "key_methods": [
        "__len",
        "Size",
        "Get"
      ]
    },
    {
      "method_id": "m002",
      "summary": "尝试按索引获取卡片配置，但由于 bug 返回无效的 userdata，目前无法正常使用。",
      "use_cases": [
        "本意是获取指定卡片配置，但当前无效"
      ],
      "key_methods": [
        "Get",
        "__len",
        "Size"
      ]
    },
    {
      "method_id": "m003",
      "summary": "只读常量，存储列表中的卡片数量，功能与 __len 完全相同。",
      "use_cases": [
        "直接读取卡片数量",
        "替代 # 操作符使用"
      ],
      "key_methods": [
        "Size",
        "__len",
        "Get"
      ]
    }
  ]
}
```
