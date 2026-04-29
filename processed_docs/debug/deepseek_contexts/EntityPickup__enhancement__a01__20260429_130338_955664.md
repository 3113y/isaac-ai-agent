# DeepSeek Context

- class: EntityPickup
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:03:38.955700

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

类名：EntityPickup

原始 md 文档（该类完整文档，可能已截断）：
# Class "EntityPickup"

???+ info

    你可以通过以下函数获取此类：

    * [Entity.ToPickup()](Entity.md#topickup)

    ???+ example "Example Code"
        `local entity = Isaac.GetRoomEntities()[1]:ToPickup()`

## Class Diagram
--8<-- "docs/snippets/EntityClassDiagram.md"
## Functions
### Appear·Fast () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AppearFast ( ) {: .copyable aria-label='Functions' }

___
### Can·Reroll () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean CanReroll ( ) {: .copyable aria-label='Functions' }

___
### Get·Coin·Value () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### int GetCoinValue ( ) {: .copyable aria-label='Functions' }
If this is a coin, return its face value, else zero.
___
### Is·Shop·Item () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsShopItem ( ) {: .copyable aria-label='Functions' }

___
### Morph () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void Morph ( [EntityType](enums/EntityType.md) Type, int Variant, int SubType, boolean KeepPrice = false, boolean KeepSeed = false, boolean IgnoreModifiers = false ) {: .copyable aria-label='Functions' }

**KeepSeed**: 如果设置为 true，将保留拾取物的初始 RNG 种子，而不是重置它

**IgnoreModifiers**: 如果设置为true，将忽略可能将此拾取物转变为其他类型的物品效果。具体来说，这可以用来防止道具受到堕化以撒的额外选择机制的影响。（例如，如果您手动生成一个任务道具，例如 Polaroid，它将受到堕化以撒的机制的影响，这通常是不可取的。要解决此问题，您可以在生成后立即将其变形为相同的实体类型/变体/子类型，并将此参数设置为 true。）
___
### Play·Drop·Sound () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void PlayDropSound ( ) {: .copyable aria-label='Functions' }

___
### Play·Pickup·Sound () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void PlayPickupSound ( ) {: .copyable aria-label='Functions' }

___
### Try·Open·Chest () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean TryOpenChest ( [EntityPlayer](EntityPlayer.md) Player = nil ) {: .copyable aria-label='Functions' }
**Player**: The player that opened this chest
___
## Variables
### Auto·Update·Price {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean AutoUpdatePrice  {: .copyable aria-label='Variables' }

___
### Charge {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Charge  {: .copyable aria-label='Variables' }

___
### OptionsPickupIndex {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int OptionsPickupIndex  {: .copyable aria-label='Variables' }

任何非 0 的值都会导致该物品与任何其他具有相同 OptionsPickupIndex 值的物品形成选项组。

当属于选项组的物品被拾取时，所有属于同一组的其他物品都会消失。

0 是默认值，表示该物品不属于任何组。
___
### Price {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Price  {: .copyable aria-label='Variables' }
该物品在商店中的价格。

???- info "堕化店长信息"

    在堕化店长身上，所有物品都应该有一个价格。但是，任何使用 Lua 生成的物品都不符合此规则，因此您必须手动设置价格。在分配价格的下一帧（例如 `1`）之后，它将自动调整为堕化店长的正确价格（例如 15）。这是由于 AutoUpdatePrice 功能造成的。

    该方法在大多数情况下都有效。然而，它在特殊房间（例如天使房）中会出现问题，有时价格会跳到错误的值，例如 24、99 等。解决此问题的方法是将 ShopItemId 设置为任意负值（例如 -1）。

___
### Shop·Item·Id {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ShopItemId  {: .copyable aria-label='Variables' }

如果在商店中, 这个值描述了这个物品在商店的哪一个槽中售卖。例如，如果商店有 6 个待售物品，则房间中的拾取物将具有 0、1、2、3、4 和 5 的商店物品 ID。

当生成一个新的道具时，ShopItemId 默认为 0。这会导致 D6 将道具重置为红心。通过将商店物品 ID 设置为 -1，可以修复此行为，使道具正确重置为另一个道具。然而，非道具可能会通过 D20 或类似物品重置为道具。

通过将商店物品 ID 设置为 -2，自动价格将为恶魔交易价格。否则，这与 -1 相同。

其他负值的行为与 -1 相同。

___
### State {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int State  {: .copyable aria-label='Variables' }

___
### Timeout {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Timeout  {: .copyable aria-label='Variables' }

使拾取物在一段时间后闪烁并消失，就像堕化玛姬掉落的临时生命值一样。该值每帧减少 1，达到 0 后拾取物消失。如果 Timeout 设置为 -1（正常拾取物的默认值），则拾取物将正常工作而不会消失。

___
### Touched {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean Touched  {: .copyable aria-label='Variables' }

___
### Wait {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Wait  {: .copyable aria-label='Variables' }

被用于道具，以强制执行一段时间，期间玩家将不会自动拾取道具。新的道具生成时，`Wait` 值为 20（对应于 20 帧游戏时间）。该值会随着游戏帧的推移而自动减少。

目前尚不清楚此值是否用于其他类型的拾取物。

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "AppearFast",
    "signature": "void AppearFast ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "CanReroll",
    "signature": "boolean CanReroll ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "GetCoinValue",
    "signature": "int GetCoinValue ( ) {: .copyable aria-label='Functions' }",
    "description": "If this is a coin, return its face value, else zero."
  },
  {
    "method_id": "m004",
    "name": "IsShopItem",
    "signature": "boolean IsShopItem ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "Morph",
    "signature": "void Morph ( [EntityType](enums/EntityType.md) Type, int Variant, int SubType, boolean KeepPrice = false, boolean KeepSeed = false, boolean IgnoreModifiers = false ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "PlayDropSound",
    "signature": "void PlayDropSound ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "PlayPickupSound",
    "signature": "void PlayPickupSound ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "TryOpenChest",
    "signature": "boolean TryOpenChest ( [EntityPlayer](EntityPlayer.md) Player = nil ) {: .copyable aria-label='Functions' }",
    "description": "**Player**: The player that opened this chest"
  },
  {
    "method_id": "m009",
    "name": "AutoUpdatePrice",
    "signature": "boolean AutoUpdatePrice  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "Charge",
    "signature": "int Charge  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "OptionsPickupIndex",
    "signature": "int OptionsPickupIndex  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "Price",
    "signature": "int Price  {: .copyable aria-label='Variables' }",
    "description": "该物品在商店中的价格。"
  },
  {
    "method_id": "m013",
    "name": "ShopItemId",
    "signature": "int ShopItemId  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "State",
    "signature": "int State  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "Timeout",
    "signature": "int Timeout  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m016",
    "name": "Touched",
    "signature": "boolean Touched  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m017",
    "name": "Wait",
    "signature": "int Wait  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "EntityPickup 表示游戏中的可拾取物品实体，如硬币、心、炸弹、钥匙、宝箱、道具等。可通过 Entity:ToPickup() 将实体转换为拾取物操作接口，提供变形、价格控制、拾取行为、音效、箱子开启等功能。",
    "use_cases": [
      "在房间内动态创建或修改拾取物类型和属性",
      "定制商店物品的价格、选项组和重置行为",
      "实现宝箱打开逻辑及对应的玩家交互",
      "控制拾取物的生成动画、消失倒计时和拾取冷却",
      "查询拾取物能否重掷、是否为商店物品或获取硬币面值"
    ],
    "key_methods": [
      "Morph",
      "TryOpenChest",
      "AppearFast",
      "CanReroll",
      "IsShopItem"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "使拾取物立即以快速动画出现（跳过正常渐现过程）。",
      "use_cases": [
        "动态生成拾取物时使玩家能立即看见并拾取",
        "修复因延迟出现导致的奇怪显示问题"
      ],
      "key_methods": [
        "AppearFast",
        "Morph",
        "Wait",
        "Timeout"
      ]
    },
    {
      "method_id": "m002",
      "summary": "查询该拾取物是否可以被重掷（如被 D6 等道具影响）。",
      "use_cases": [
        "判断拾取物是否受重掷效果影响，用于自定义重掷逻辑",
        "在重掷前过滤出不可重掷的拾取物以避免错误"
      ],
      "key_methods": [
        "CanReroll",
        "Morph",
        "ShopItemId"
      ]
    },
    {
      "method_id": "m003",
      "summary": "若当前拾取物为硬币，返回其面值；否则返回 0。",
      "use_cases": [
        "获取硬币的金额以用于金钱统计或自定义交易",
        "区分不同硬币面值实现特定机制"
      ],
      "key_methods": [
        "GetCoinValue",
        "Morph",
        "Price"
      ]
    },
    {
      "method_id": "m004",
      "summary": "返回该拾取物是否为商店中待售的物品。",
      "use_cases": [
        "检测拾取物是否属于商店布局，以便修改价格或行为",
        "在商店重掷时区分普通掉落和商店物品"
      ],
      "key_methods": [
        "IsShopItem",
        "ShopItemId",
        "Price",
        "AutoUpdatePrice"
      ]
    },
    {
      "method_id": "m005",
      "summary": "将当前拾取物变形为指定的实体类型、变体和子类型，可选择保留价格、保留 RNG 种子或忽略外在修改效果（如堕化以撒的额外选择）。常用于生成自定义拾取物或纠正被全局效果扭曲的拾取物。",
      "use_cases": [
        "动态改变拾取物类型，如将普通硬币变成幸运硬币",
        "生成任务关键道具时防止被角色被动效果改变",
        "保留价格实现商店物品类型替换而不重置价格",
        "使用 KeepSeed 保持随机性一致，适用于伪随机环境"
      ],
      "key_methods": [
        "Morph",
        "AppearFast",
        "CanReroll",
        "AutoUpdatePrice",
        "ShopItemId"
      ]
    },
    {
      "method_id": "m006",
      "summary": "播放拾取物掉落时的音效。",
      "use_cases": [
        "在自定义生成拾取物时模拟自然掉落声音",
        "结合 Morph 等操作保持视听一致性"
      ],
      "key_methods": [
        "PlayDropSound",
        "PlayPickupSound",
        "AppearFast"
      ]
    },
    {
      "method_id": "m007",
      "summary": "播放拾取物被捡起时的音效。",
      "use_cases": [
        "手动触发拾取时播放对应音效，提升反馈感",
        "实现特殊拾取事件而不触发默认的自动拾取逻辑"
      ],
      "key_methods": [
        "PlayPickupSound",
        "PlayDropSound"
      ]
    },
    {
      "method_id": "m008",
      "summary": "尝试使用指定玩家打开此拾取物宝箱。若成功返回 true，通常用于触发宝箱内容物生成。",
      "use_cases": [
        "自定义宝箱开启逻辑（如需要钥匙判定、动画）",
        "通过玩家参考实现多人模式下正确的宝箱归属"
      ],
      "key_methods": [
        "TryOpenChest",
        "Morph",
        "State"
      ]
    },
    {
      "method_id": "m009",
      "summary": "布尔变量，控制是否自动根据游戏规则更新拾取物价格（例如堕化店长的价格修正）。默认开启。",
      "use_cases": [
        "关闭自动价格更新以实现自定义定价",
        "在生成商店物品后立即手动设定价格并防止被覆盖"
      ],
      "key_methods": [
        "AutoUpdatePrice",
        "Price",
        "ShopItemId"
      ]
    },
    {
      "method_id": "m010",
      "summary": "整数变量，记录携带电池的充能数（通常用于电池类拾取物）。",
      "use_cases": [
        "设置或获取电池拾取物的充能值",
        "使自定义电池物品提供特定的充能量"
      ],
      "key_methods": [
        "Charge",
        "Morph"
      ]
    },
    {
      "method_id": "m011",
      "summary": "非零整数值，使该拾取物与相同 OptionsPickupIndex 的其它拾取物形成选项组。当一个被拾取时，同组其它物品消失。",
      "use_cases": [
        "创建二选一或多选一的拾取物组，类似游戏内选项道具",
        "实现自定义房间机制时强制互斥拾取"
      ],
      "key_methods": [
        "OptionsPickupIndex",
        "Touched"
      ]
    },
    {
      "method_id": "m012",
      "summary": "该拾取物在商店中的价格（整数）。仅当拾取物位于商店摊位时生效，配合 AutoUpdatePrice 可被自动修正。",
      "use_cases": [
        "设置或修改商店物品的售价",
        "动态定价或折扣机制"
      ],
      "key_methods": [
        "Price",
        "AutoUpdatePrice",
        "ShopItemId",
        "IsShopItem"
      ]
    },
    {
      "method_id": "m013",
      "summary": "商店物品槽 ID，用于标识该拾取物属于商店的哪个货架位置，并影响重置行为。设为 -1 可避免被 D6 重置为红心，-2 则采用恶魔交易价格自动定价。",
      "use_cases": [
        "修复 Lua 生成商店物品被错误重置的问题",
        "设定恶魔交易价格风格（设定为 -2）"
      ],
      "key_methods": [
        "ShopItemId",
        "Price",
        "AutoUpdatePrice",
        "IsShopItem"
      ]
   
```
