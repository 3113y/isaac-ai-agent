# DeepSeek Context

- class: TemporaryEffect
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T14:16:02.899948

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

类名：TemporaryEffect

原始 md 文档（该类完整文档，可能已截断）：
# Class "TemporaryEffect"

???+ info
    You can get this class by using the following functions:

    * [TemporaryEffects:GetCollectibleEffect()](TemporaryEffects.md#getcollectibleeffect)
    * [TemporaryEffects:GetNullEffect()](TemporaryEffects.md#getnulleffect)
    * [TemporaryEffects:GetTrinketEffect()](TemporaryEffects.md#gettrinketeffect)

    ???+ example "Example Code"
        ```lua
        local player = Isaac.GetPlayer()
        local tempEffects = player:GetEffects()
        local tempEffect = tempEffects:GetCollectibleEffect(CollectibleType.COLLECTIBLE_SAD_ONION)
        ```

## Variables
### Cooldown {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Cooldown  {: .copyable aria-label='Variables' }

___
### Count {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Count  {: .copyable aria-label='Variables' }

___
### Item {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [ItemConfig Item](ItemConfig_Item.md) Item {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "Cooldown",
    "signature": "int Cooldown  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "Count",
    "signature": "int Count  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "Item",
    "signature": "[ItemConfig Item](ItemConfig_Item.md) Item {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "TemporaryEffect 表示一个临时的道具或饰品效果实例，包含其冷却时间、叠加层数以及对应的物品配置数据。",
    "use_cases": [
      "获取临时效果的剩余冷却时间",
      "判断临时效果的当前叠加层数",
      "关联效果与具体物品配置"
    ],
    "key_methods": [
      "Cooldown",
      "Count",
      "Item"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "获取该临时效果的当前冷却时间（帧数）。",
      "use_cases": [
        "检查临时效果是否仍处于冷却中",
        "实现基于冷却时间的 UI 指示器"
      ],
      "key_methods": [
        "Cooldown",
        "Count",
        "Item"
      ]
    },
    {
      "method_id": "m002",
      "summary": "获取该临时效果的当前叠加层数。",
      "use_cases": [
        "判断临时效果的强度等级",
        "控制效果叠加时的行为变化"
      ],
      "key_methods": [
        "Count",
        "Cooldown",
        "Item"
      ]
    },
    {
      "method_id": "m003",
      "summary": "获取与该临时效果关联的物品配置项（ItemConfig Item）。",
      "use_cases": [
        "检索效果来源的完整物品数据",
        "区分不同道具生成的同类临时效果"
      ],
      "key_methods": [
        "Item",
        "Cooldown",
        "Count"
      ]
    }
  ]
}
```
