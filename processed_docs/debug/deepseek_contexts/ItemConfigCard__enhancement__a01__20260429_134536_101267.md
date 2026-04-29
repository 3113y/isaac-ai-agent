# DeepSeek Context

- class: ItemConfigCard
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:45:36.101348

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

类名：ItemConfigCard

原始 md 文档（该类完整文档，可能已截断）：
# Class "ItemConfigCard"

???+ info
    You can get this class by using the following function:

    * [ItemConfig.GetCard()](ItemConfig.md#getcard)

    ???+ example "Example Code"
        `Isaac.GetItemConfig():GetCard(Card.CARD_FOOL)`

## Functions
___
### Is·Available () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean IsAvailable ( ) {: .copyable aria-label='Functions' }

___
### Is·Card () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean IsCard ( ) {: .copyable aria-label='Functions' }

___
### Is·Rune () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean IsRune ( ) {: .copyable aria-label='Functions' }

___
## Variables
### Achievement·ID {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AchievementID  {: .copyable aria-label='Variables' }
Returns the ID of the achievement that unlocks the card. Returns ``:::lua -1`` if the card is unlocked by default.

___
### Announcer·Delay {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int AnnouncerDelay  {: .copyable aria-label='Variables' }

___
### Announcer·Voice {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int AnnouncerVoice  {: .copyable aria-label='Variables' }

___
### Card·Type {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int CardType {: .copyable aria-label='Variables' }

___
### Description {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string Description  {: .copyable aria-label='Variables' }

Returns the description of the card.

???- warning "Warning"
    In Repentance, this function now returns ``#[CARD_NAME]_DESCRIPTION``
___
### Greed·Mode·Allowed {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean GreedModeAllowed  {: .copyable aria-label='Variables' }

Returns whether or not the item can appear in Greed or Greedier mode.
___
### Hud·Anim {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string HudAnim  {: .copyable aria-label='Variables' }

Returns the name of the animation in `ui_cardfronts.anm2`.

???- bug "Bugs"
    This will return a blank string unless used on a modded card. Standard cards will return nothing.
___
### ID {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ID  {: .copyable aria-label='Variables' }

Returns the ID of the given card.
___
### Mimic·Charge {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int MimicCharge {: .copyable aria-label='Variables' }

___
### Name {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string Name  {: .copyable aria-label='Variables' }

Returns the name of the given card.
???- warning "Warning"
    In Repentance, this function now returns ``#[CARD_NAME]_NAME``

___
### Pickup·Subtype {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int PickupSubtype {: .copyable aria-label='Variables' }

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
    "name": "IsCard",
    "signature": "boolean IsCard ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "IsRune",
    "signature": "boolean IsRune ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "AchievementID",
    "signature": "int AchievementID  {: .copyable aria-label='Variables' }",
    "description": "Returns the ID of the achievement that unlocks the card. Returns ``:::lua -1`` if the card is unlocked by default."
  },
  {
    "method_id": "m005",
    "name": "AnnouncerDelay",
    "signature": "int AnnouncerDelay  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "AnnouncerVoice",
    "signature": "int AnnouncerVoice  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "CardType",
    "signature": "int CardType {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "Description",
    "signature": "string Description  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "GreedModeAllowed",
    "signature": "boolean GreedModeAllowed  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "HudAnim",
    "signature": "string HudAnim  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "ID",
    "signature": "int ID  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "MimicCharge",
    "signature": "int MimicCharge {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "Name",
    "signature": "string Name  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "PickupSubtype",
    "signature": "int PickupSubtype {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "ItemConfigCard 封装卡牌/符文的配置数据，包括名称、描述、解锁状态、类型标识及动画等元信息。",
    "use_cases": [
      "获取卡牌的显示名称和描述文本",
      "判断卡牌是否在贪婪模式中可用",
      "确定卡牌类型的布尔检查（卡牌、符文、整体可用性）",
      "读取解锁成就ID以决定掉落逻辑"
    ],
    "key_methods": [
      "IsCard",
      "IsRune",
      "IsAvailable",
      "Name",
      "ID"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "返回布尔值，判断该卡牌整体是否可用（例如已解锁或满足出现条件）。",
      "use_cases": [
        "在生成掉落前过滤不可用卡牌",
        "决定某些成就或解锁机制是否触发"
      ],
      "key_methods": [
        "IsAvailable",
        "AchievementID",
        "GreedModeAllowed",
        "ID"
      ]
    },
    {
      "method_id": "m002",
      "summary": "返回布尔值，表示该卡牌是否为普通卡牌（而非符文或其它类型）。",
      "use_cases": [
        "区分卡牌属类以应用不同效果",
        "在UI中按类别分组显示"
      ],
      "key_methods": [
        "IsCard",
        "IsRune",
        "CardType",
        "ID"
      ]
    },
    {
      "method_id": "m003",
      "summary": "返回布尔值，表示该卡牌是否为符文。",
      "use_cases": [
        "单独处理符文类物品的逻辑",
        "在成就追踪时区分符文与普通卡牌"
      ],
      "key_methods": [
        "IsRune",
        "IsCard",
        "CardType",
        "Name"
      ]
    },
    {
      "method_id": "m004",
      "summary": "返回解锁此卡牌所需成就的ID，若默认可用则返回 -1。",
      "use_cases": [
        "检查卡牌是否通过成就解锁",
        "决定商店或掉落表是否需要成就前置"
      ],
      "key_methods": [
        "AchievementID",
        "IsAvailable",
        "ID",
        "Name"
      ]
    },
    {
      "method_id": "m005",
      "summary": "获取播报员播放卡牌名称的延迟时间（整数）。",
      "use_cases": [
        "调节自定义播报音效的时机"
      ],
      "key_methods": [
        "AnnouncerDelay",
        "AnnouncerVoice",
        "Name"
      ]
    },
    {
      "method_id": "m006",
      "summary": "获取与卡牌关联的播报员语音ID。",
      "use_cases": [
        "播放特定语音响应卡牌使用或获得"
      ],
      "key_methods": [
        "AnnouncerVoice",
        "AnnouncerDelay",
        "Name"
      ]
    },
    {
      "method_id": "m007",
      "summary": "返回表示卡牌类型的整数值（例如普通卡牌、符文等）。",
      "use_cases": [
        "在不依赖布尔方法时进行分类型逻辑",
        "存储或比较不同类型的卡牌"
      ],
      "key_methods": [
        "CardType",
        "IsCard",
        "IsRune",
        "ID"
      ]
    },
    {
      "method_id": "m008",
      "summary": "返回卡牌的描述文本。在 Repentance 中返回的是本地化键名（如 #[CARD_NAME]_DESCRIPTION）。",
      "use_cases": [
        "在UI中显示卡牌描述",
        "通过键名进行本地化翻译"
      ],
      "key_methods": [
        "Description",
        "Name",
        "ID",
        "HudAnim"
      ]
    },
    {
      "method_id": "m009",
      "summary": "返回布尔值，指示该卡牌是否允许在贪婪/超级贪婪模式中出现。",
      "use_cases": [
        "生成贪婪模式专属掉落表",
        "过滤不适用的卡牌避免错误出现"
      ],
      "key_methods": [
        "GreedModeAllowed",
        "IsAvailable",
        "ID"
      ]
    },
    {
      "method_id": "m010",
      "summary": "返回卡片正面动画的名称（在 ui_cardfronts.anm2 中）。对标准卡牌返回空字符串，仅在模组卡牌上有效。",
      "use_cases": [
        "加载自定义卡牌动画",
        "在HUD上渲染特殊卡面效果"
      ],
      "key_methods": [
        "HudAnim",
        "Name",
        "Description"
      ]
    },
    {
      "method_id": "m011",
      "summary": "返回该卡牌的唯一整数ID。",
      "use_cases": [
        "比对不同卡牌",
        "通过ID获取对应配置进行批量处理"
      ],
      "key_methods": [
        "ID",
        "Name",
        "IsCard",
        "IsRune"
      ]
    },
    {
      "method_id": "m012",
      "summary": "返回模仿（Mimic）相关充能数，具体含义视上下文而定。",
      "use_cases": [
        "控制模仿效果或类似机制的充能消耗"
      ],
      "key_methods": [
        "MimicCharge",
        "IsCard",
        "CardType"
      ]
    },
    {
      "method_id": "m013",
      "summary": "返回卡牌的名称。在 Repentance 中返回的是本地化键名（如 #[CARD_NAME]_NAME）。",
      "use_cases": [
        "获取用于显示的卡牌名称",
        "通过键名实现多语言支持"
      ],
      "key_methods": [
        "Name",
        "Description",
        "ID",
        "HudAnim"
      ]
    },
    {
      "method_id": "m014",
      "summary": "返回拾取物的子类型，可能与卡牌效果或生成基类对应。",
      "use_cases": [
        "确定生成掉落时的拾取物类型",
        "在拾取时触发特定子类型逻辑"
      ],
      "key_methods": [
        "PickupSubtype",
        "CardType",
        "ID"
      ]
    }
  ]
}
```
