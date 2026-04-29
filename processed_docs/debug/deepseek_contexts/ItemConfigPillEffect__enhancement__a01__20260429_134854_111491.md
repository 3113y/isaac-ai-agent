# DeepSeek Context

- class: ItemConfigPillEffect
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:48:54.111524

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

类名：ItemConfigPillEffect

原始 md 文档（该类完整文档，可能已截断）：
# Class "ItemConfigPillEffect"

???+ info
    You can get this class by using the following function:

    * [ItemConfig.GetPillEffect()](ItemConfig.md#getpilleffect)

    ???+ example "Example Code"
        `Isaac.GetItemConfig():GetPillEffect(PillEffect.PILLEFFECT_BAD_GAS)`

## Functions
___
### Is·Available () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean IsAvailable ( ) {: .copyable aria-label='Functions' }

___
## Variables
### Achievement·ID {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AchievementID  {: .copyable aria-label='Variables' }

The ID of the achievement that unlocks the pill effect. Returns ``:::lua -1`` by default.
___
### Announcer·Delay {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int AnnouncerDelay  {: .copyable aria-label='Variables' }

___
### Announcer·Voice {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int AnnouncerVoice  {: .copyable aria-label='Variables' }

___
### Announcer·Voice·Super {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int AnnouncerVoiceSuper  {: .copyable aria-label='Variables' }

___
### Effect·Class {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int EffectClass  {: .copyable aria-label='Variables' }
???+ bug "Bug"
    This variable is broken and returns userdata.

___
### Effect·Sub·Class {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int EffectSubClass  {: .copyable aria-label='Variables' }
???+ bug "Bug"
    This variable is broken and returns userdata.

___
### Greed·Mode·Allowed {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean GreedModeAllowed  {: .copyable aria-label='Variables' }

Returns if the pill effect is allowed in Greed mode. Returns ``:::lua true`` by default.
___
### ID {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ID  {: .copyable aria-label='Variables' }

Returns the pill effect's ID.
___
### Mimic·Charge {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int MimicCharge  {: .copyable aria-label='Variables' }

___
### Name {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string Name  {: .copyable aria-label='Variables' }

Returns the name of the pill effect.

???- warning "Warning"
    In Repentance, returns "#[PILL_NAME]" rather than the pill effect's ingame name. (i.e. Balls of Steel will return #BALLS_OF_STEEL_NAME)
___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "IsAvailable",
    "signature": "boolean IsAvailable ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "AchievementID",
    "signature": "int AchievementID  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "AnnouncerDelay",
    "signature": "int AnnouncerDelay  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "AnnouncerVoice",
    "signature": "int AnnouncerVoice  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "AnnouncerVoiceSuper",
    "signature": "int AnnouncerVoiceSuper  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "EffectClass",
    "signature": "int EffectClass  {: .copyable aria-label='Variables' }",
    "description": "???+ bug \"Bug\""
  },
  {
    "method_id": "m007",
    "name": "EffectSubClass",
    "signature": "int EffectSubClass  {: .copyable aria-label='Variables' }",
    "description": "???+ bug \"Bug\""
  },
  {
    "method_id": "m008",
    "name": "GreedModeAllowed",
    "signature": "boolean GreedModeAllowed  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "ID",
    "signature": "int ID  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "MimicCharge",
    "signature": "int MimicCharge  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "Name",
    "signature": "string Name  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "代表一个药丸效果的配置信息，可通过ItemConfig.GetPillEffect()获取，提供可用性检查、解锁成就、播音员设置、ID、名称等只读属性。",
    "use_cases": [
      "检测药丸效果在当前模式是否可用",
      "获取解锁该药丸效果的成就ID",
      "读取药丸效果的内部ID与格式化名称",
      "查询药丸效果在贪婪模式是否允许出现"
    ],
    "key_methods": [
      "IsAvailable",
      "AchievementID",
      "GreedModeAllowed",
      "ID",
      "Name"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "检查该药丸效果在当前游戏环境（如模式、解锁状态）下是否可用。",
      "use_cases": [
        "在随机生成药丸前过滤不可用的效果",
        "确认特定药丸效果是否因达成条件而解锁"
      ],
      "key_methods": [
        "IsAvailable",
        "AchievementID",
        "GreedModeAllowed"
      ]
    },
    {
      "method_id": "m002",
      "summary": "返回解锁该药丸效果的成就ID，未关联成就时默认返回-1。",
      "use_cases": [
        "检查药丸效果是否已被玩家解锁",
        "追踪需要哪些成就来解锁指定药丸"
      ],
      "key_methods": [
        "AchievementID",
        "IsAvailable",
        "ID"
      ]
    },
    {
      "method_id": "m003",
      "summary": "返回与该药丸效果关联的播报员语音延迟值。",
      "use_cases": [
        "自定义或调试药丸的播报员播放时序"
      ],
      "key_methods": [
        "AnnouncerDelay",
        "AnnouncerVoice",
        "AnnouncerVoiceSuper"
      ]
    },
    {
      "method_id": "m004",
      "summary": "返回该药丸效果使用的普通播报员语音ID。",
      "use_cases": [
        "查询或读取药丸效果的播报员语音资源"
      ],
      "key_methods": [
        "AnnouncerVoice",
        "AnnouncerDelay",
        "AnnouncerVoiceSuper"
      ]
    },
    {
      "method_id": "m005",
      "summary": "返回该药丸效果使用的超级播报员语音ID。",
      "use_cases": [
        "获取药丸效果在超级播报员模式下的语音资源"
      ],
      "key_methods": [
        "AnnouncerVoiceSuper",
        "AnnouncerVoice",
        "AnnouncerDelay"
      ]
    },
    {
      "method_id": "m006",
      "summary": "原本应返回效果主类，但由于已知Bug，该变量返回userdata而非有效整数，不推荐使用。",
      "use_cases": [
        "注意避免使用此属性，它不可靠"
      ],
      "key_methods": [
        "EffectClass",
        "EffectSubClass"
      ]
    },
    {
      "method_id": "m007",
      "summary": "原本应返回效果子类，但由于已知Bug，该变量返回userdata而非有效整数，不推荐使用。",
      "use_cases": [
        "注意避免使用此属性，它不可靠"
      ],
      "key_methods": [
        "EffectSubClass",
        "EffectClass"
      ]
    },
    {
      "method_id": "m008",
      "summary": "返回该药丸效果是否允许在贪婪模式中出现，默认为true。",
      "use_cases": [
        "在贪婪模式中过滤可用的药丸列表",
        "判断特定药丸效果在贪婪模式是否被禁用"
      ],
      "key_methods": [
        "GreedModeAllowed",
        "IsAvailable"
      ]
    },
    {
      "method_id": "m009",
      "summary": "返回药丸效果的内部标识ID。",
      "use_cases": [
        "用于精确比较或存储药丸效果",
        "作为PillEffect枚举值的直接参考"
      ],
      "key_methods": [
        "ID",
        "Name"
      ]
    },
    {
      "method_id": "m010",
      "summary": "返回与该药丸效果相关的模仿者充能数值。",
      "use_cases": [
        "查询药丸效果在模仿者机制中的充能消耗"
      ],
      "key_methods": [
        "MimicCharge"
      ]
    },
    {
      "method_id": "m011",
      "summary": "返回药丸效果的名字字符串。但在Repentance版本中，返回的是格式化的键名（如#BALLS_OF_STEEL_NAME）而非游戏内实际名称。",
      "use_cases": [
        "获取药丸效果的内部名称标识",
        "注意需要额外处理才能得到可读的游戏内名称"
      ],
      "key_methods": [
        "Name",
        "ID"
      ]
    }
  ]
}
```
