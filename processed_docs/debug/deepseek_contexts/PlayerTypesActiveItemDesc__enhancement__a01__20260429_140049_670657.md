# DeepSeek Context

- class: PlayerTypesActiveItemDesc
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T14:00:49.670689

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

类名：PlayerTypesActiveItemDesc

原始 md 文档（该类完整文档，可能已截断）：
# Class "PlayerTypesActiveItemDesc"

???+ info
    You can get this class by using the following function:

    * [EntityPlayer.SecondaryActiveItem](EntityPlayer.md#secondaryactiveitem)

    ???+ example "Example Code"
        ```lua
        local player = Isaac.GetPlayer()
        local activeItemDesc = player.SecondaryActiveItem
        ```

## Variables
### Battery·Charge {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int BatteryCharge  {: .copyable aria-label='Variables' }

___
### Charge {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Charge  {: .copyable aria-label='Variables' }
For items like Jars this holds the number of flies/hearts.
___
### Item {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [CollectibleType](enums/CollectibleType.md) Item {: .copyable aria-label='Variables' }

___
### PartialCharge {: aria-label='Variables' }
[ ](#){: .rep .tooltip .badge }
#### float PartialCharge {: .copyable aria-label='Variables' }
How close the item is to gaining another charge (0-1 range, used by 4.5 Volt)

___
### SubCharge {: aria-label='Variables' }
[ ](#){: .rep .tooltip .badge }
#### int SubCharge {: .copyable aria-label='Variables' }

___
### TimedRechargeCooldown {: aria-label='Variables' }
[ ](#){: .rep .tooltip .badge }
#### int TimedRechargeCooldown {: .copyable aria-label='Variables' }
Number of frames before an item with a timed cooldown can recharge again (used by Spin To Win to pause its recharge after fully discharging it)
___
### VarData {: aria-label='Variables' }
[ ](#){: .rep .tooltip .badge }
#### int VarData {: .copyable aria-label='Variables' }
Holds extra information for some active items (such as the number of uses for Jar of Wisps)
___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "BatteryCharge",
    "signature": "int BatteryCharge  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "Charge",
    "signature": "int Charge  {: .copyable aria-label='Variables' }",
    "description": "For items like Jars this holds the number of flies/hearts."
  },
  {
    "method_id": "m003",
    "name": "Item",
    "signature": "[CollectibleType](enums/CollectibleType.md) Item {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "PartialCharge",
    "signature": "float PartialCharge {: .copyable aria-label='Variables' }",
    "description": "How close the item is to gaining another charge (0-1 range, used by 4.5 Volt)"
  },
  {
    "method_id": "m005",
    "name": "SubCharge",
    "signature": "int SubCharge {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "TimedRechargeCooldown",
    "signature": "int TimedRechargeCooldown {: .copyable aria-label='Variables' }",
    "description": "Number of frames before an item with a timed cooldown can recharge again (used by Spin To Win to pause its recharge after fully discharging it)"
  },
  {
    "method_id": "m007",
    "name": "VarData",
    "signature": "int VarData {: .copyable aria-label='Variables' }",
    "description": "Holds extra information for some active items (such as the number of uses for Jar of Wisps)"
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "表示玩家所持主动道具的状态信息，记录充能、电池充能、物品类型及额外数据。",
    "use_cases": [
      "获取/修改主动道具充能计数与部分充能进度",
      "检查当前装备的主动道具类型",
      "管理特殊道具的内部数据（如罐子容量、精灵罐次数）",
      "控制定时充能道具的冷却间隔（如Spin To Win）",
      "实现自定义充能逻辑或特殊道具行为"
    ],
    "key_methods": [
      "Charge",
      "Item",
      "PartialCharge",
      "VarData",
      "BatteryCharge"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "表示从电池拾取中获得的额外充能值，独立于主充能计数。",
      "use_cases": [
        "获取当前电池额外充能力度",
        "修改电池补充量以自定义电池效果",
        "计算道具总充能状态"
      ],
      "key_methods": [
        "BatteryCharge",
        "Charge",
        "PartialCharge",
        "Item"
      ]
    },
    {
      "method_id": "m002",
      "summary": "表示主动道具的主充能次数，对罐子类道具也用于存储内含物数量。",
      "use_cases": [
        "读取道具剩余使用次数",
        "直接设置充能以修改道具行为",
        "检查罐子类道具内收集的苍蝇或心数"
      ],
      "key_methods": [
        "Charge",
        "Item",
        "PartialCharge",
        "VarData"
      ]
    },
    {
      "method_id": "m003",
      "summary": "表示当前所持主动道具的物品类型，用于识别具体道具。",
      "use_cases": [
        "判断玩家当前装备的主动道具",
        "基于道具类型编写条件逻辑",
        "在主动道具切换后同步相关数据"
      ],
      "key_methods": [
        "Item",
        "Charge",
        "VarData"
      ]
    },
    {
      "method_id": "m004",
      "summary": "表示充能的分数进度（0-1），用于实现平滑充能显示和4.5伏特等效果。",
      "use_cases": [
        "实现自定义充能条动画",
        "配合4.5伏特计算额外充能增量",
        "控制部分充能的视觉反馈"
      ],
      "key_methods": [
        "PartialCharge",
        "Charge",
        "TimedRechargeCooldown"
      ]
    },
    {
      "method_id": "m005",
      "summary": "表示某些道具使用的子充能计数，具体含义因道具而异。",
      "use_cases": [
        "读取具有子充能系统的道具状态",
        "修改子充能以实现多阶段道具行为",
        "辅助复杂充能道具的数据管理"
      ],
      "key_methods": [
        "SubCharge",
        "Charge",
        "Item",
        "VarData"
      ]
    },
    {
      "method_id": "m006",
      "summary": "表示定时充能道具的当前冷却帧数，用于暂停充能（如Spin To Win完全消耗后）。",
      "use_cases": [
        "获取或设置道具的充能冷却时间",
        "实现类似Spin To Win的间歇充能机制",
        "防止道具在冷却期间被重复使用"
      ],
      "key_methods": [
        "TimedRechargeCooldown",
        "Charge",
        "PartialCharge"
      ]
    },
    {
      "method_id": "m007",
      "summary": "存储主动道具的额外自定义数据，如Jar of Wisps的剩余使用次数。",
      "use_cases": [
        "读取特定道具的额外状态信息",
        "修改额外数据以扩展道具功能",
        "实现类似精灵罐计数等自定义机制"
      ],
      "key_methods": [
        "VarData",
        "Item",
        "Charge",
        "SubCharge"
      ]
    }
  ]
}
```
