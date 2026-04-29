# DeepSeek Context

- class: QueueItemData
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T14:03:38.889670

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

类名：QueueItemData

原始 md 文档（该类完整文档，可能已截断）：
# Class "QueueItemData"

???+ info
    You can get this class by using the following function:

    * [EntityPlayer.QueuedItem](EntityPlayer.md#queueditem)

    ???+ example "Example Code"
        ```lua
        local player = Isaac.GetPlayer()
        local queueItemData = player.QueuedItem
        ```

## Variables
### Charge {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Charge {: .copyable aria-label='Variables' }

___
### Item {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [ItemConfig Item](ItemConfig_Item.md) Item {: .copyable aria-label='Variables' }

___
### Touched {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean Touched {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "Charge",
    "signature": "int Charge {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "Item",
    "signature": "[ItemConfig Item](ItemConfig_Item.md) Item {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "Touched",
    "signature": "boolean Touched {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "代表玩家排队中的道具数据，包含充能状态、道具配置信息和是否已触摸的标记。",
    "use_cases": [
      "获取当前排队道具的充能值",
      "获取排队道具的详细配置信息",
      "判断玩家是否已经触摸过排队道具"
    ],
    "key_methods": [
      "Charge",
      "Item",
      "Touched"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "排队道具当前的充能数值，用于判断道具是否可用或显示充能状态。",
      "use_cases": [
        "检查排队道具是否充满能量",
        "在UI中绘制充能进度条"
      ],
      "key_methods": [
        "Charge",
        "Item"
      ]
    },
    {
      "method_id": "m002",
      "summary": "返回排队道具的 ItemConfig_Item 对象，提供该道具的完整配置信息。",
      "use_cases": [
        "获取排队道具的ID或类型",
        "显示排队道具的图标或名称"
      ],
      "key_methods": [
        "Item",
        "Charge",
        "Touched"
      ]
    },
    {
      "method_id": "m003",
      "summary": "表示玩家是否已经触摸过该排队道具，通常用于决定是否触发拾取行为。",
      "use_cases": [
        "判断是否可以自动拾取排队道具",
        "控制排队道具的可交互状态"
      ],
      "key_methods": [
        "Touched",
        "Item"
      ]
    }
  ]
}
```
