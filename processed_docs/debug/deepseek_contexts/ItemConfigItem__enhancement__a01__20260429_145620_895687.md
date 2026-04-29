# DeepSeek Context

- class: ItemConfigItem
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 10200
- temperature: 0.2
- timestamp: 2026-04-29T14:56:20.895771

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

类名：ItemConfigItem

原始 md 文档（该类完整文档，可能已截断）：
# Class "ItemConfigItem"

???+ info
    You can get this class by using the following function:

    * [ItemConfig.GetCollectible()](ItemConfig.md#getcollectible)
    * [ItemConfig.GetNullItem()](ItemConfig.md#getnullitem)
    * [ItemConfig.GetTrinket()](ItemConfig.md#gettrinket)
    * [QueueItemData.Item](QueueItemData.md#item)
    * [TemporaryEffect.Item](TemporaryEffect.md#item)

    ???+ example "Example Code"
        `Isaac.GetItemConfig():GetCollectible(CollectibleType.COLLECTIBLE_SAD_ONION)`

## Functions
___
### Has·Tags () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean HasTags ( int Tags ) {: .copyable aria-label='Functions' }

Returns true or false, depending on whether or not the item has the given [tag](enums/ItemConfig.md).

???- example "Example Code"
    Returns if The Sad Onion has the tag "Bob" (for the Bob transformation)
    ```lua
    Isaac.GetItemConfig():GetCollectible(1):HasTags(ItemConfig.TAG_BOB)
    ```
___
### Is·Available () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean IsAvailable ( ) {: .copyable aria-label='Functions' }

Returns true if the item has been unlocked.
Returns false if item has not been unlocked or if the item has been blocked from the run by item [tags](enums/ItemConfig.md).
___
### Is·Collectible () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsCollectible ( ) {: .copyable aria-label='Functions' }

Returns if the item is a collectible.
___
### Is·Null () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsNull ( ) {: .copyable aria-label='Functions' }

Returns if the item is null.
___
### Is·Trinket () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsTrinket ( ) {: .copyable aria-label='Functions' }

Returns if the item is a trinket.
___
## Variables
### Achievement·ID {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AchievementID  {: .copyable aria-label='Variables' }

Returns the ID of the achievement that unlocks the item. Returns ``:::lua -1`` if the item is unlocked by default.
___
### Add·Black·Hearts {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AddBlackHearts  {: .copyable aria-label='Variables' }

Returns the number of black hearts the item adds to the player. 1 unit is one half black heart.
___
### Add·Bombs {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AddBombs  {: .copyable aria-label='Variables' }

Returns the number of bombs the item adds to the player.
___
### Add·Coins {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AddCoins  {: .copyable aria-label='Variables' }

Returns the number of coins the item adds to the player.
___
### Add·Costume·On·Pickup {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean AddCostumeOnPickup  {: .copyable aria-label='Variables' }

Returns whether or not the item adds its costume on pickup.
___
### Add·Hearts {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AddHearts  {: .copyable aria-label='Variables' }

Returns the number of red hearts the item heals the player by. 1 unit is one half red heart.
___
### Add·Keys {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AddKeys  {: .copyable aria-label='Variables' }

Returns the number of keys the item adds to the player.
___
### Add·Max·Hearts {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AddMaxHearts  {: .copyable aria-label='Variables' }

Returns the number of empty heart containters the item adds to the player. 1 unit is one half red heart.
___
### Add·Soul·Hearts {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int AddSoulHearts  {: .copyable aria-label='Variables' }

Returns the number of soul hearts the item adds to the player. 1 unit is one half soul heart.
___
### Cache·Flags {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int CacheFlags  {: .copyable aria-label='Variables' }

Returns the [CacheFlags](enums/CacheFlag.md) set by the item.
___
### Charge·Type {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int ChargeType  {: .copyable aria-label='Variables' }

The ChargeType of the item, shown in [items.xml](xml/items.md). If the item has no defined ChargeType, it will return ``:::lua 0``

???- note "Charge Types"
    ```lua
    0: Normal
    1: Timed
    2: Special
    ```
___
### Clear·Effects·On·Remove {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean ClearEffectsOnRemove  {: .copyable aria-label='Variables' }

Returns whether or not the item's effects should be removed when the item is removed.
___
### Costume {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [Costume](ItemConfig_Costume.md) Costume {: .copyable aria-label='Variables' }

Returns the costume given to the player by the item.
___
### CraftingQuality {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int CraftingQuality  {: .copyable aria-label='Variables' }

The item's quality for the Bag of Crafting algorithm. Possible values are -1, 0, 1, 2, 3, and 4. A value of -1 indicates that the item is disabled from being craftable.
___
### Description {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string Description  {: .copyable aria-label='Variables' }

Returns the item's description.

???- warning "Warning"
    In Repentance, returns "#[ITEM_DESCRIPTION]" rather than the item's ingame description. (i.e. The Sad Onion will return #THE_SAD_ONION_DESCRIPTION)
___
### Devil·Price {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int DevilPrice  {: .copyable aria-label='Variables' }

Returns the amount of hearts an item would cost at a devil deal. 1 unit is a full red heart.
Any item that is not marked with a devil price will return ``:::lua 1``

???- example "Example Code"
    Returns the number of hearts brimstone would cost at a devil deal.
    ```lua
    Isaac.GetItemConfig():GetCollectible(118).DevilPrice
    ```
___
### Discharged {: aria-label='Variables' }
[ ](#){: .abp .tooltip .badge }
#### boolean Discharged  {: .copyable aria-label='Variables' }
This attribute got removed with Repentance.
___
### Gfx·File·Name {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string GfxFileName  {: .copyable aria-label='Variables' }

Returns the path to the item's GFX.
___
### Hidden {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean Hidden  {: .copyable aria-label='Variables' }

Returns if the item can appear in Death Certificate area. If ``:::lua true`` the item will not appear.
___
### ID {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ID  {: .copyable aria-label='Variables' }

Returns the item's ID.
___
### Init·Charge {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int InitCharge  {: .copyable aria-label='Variables' }

Returns how much charge the item should have when picked up. ``:::lua -1`` indicates the item is fully charged when collected.

___
### Max·Charges {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int MaxCharges  {: .copyable aria-label='Variables' }

The maximum number of charges an active item could have.
___
### Max·Cooldown {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int MaxCooldown  {: .copyable aria-label='Variables' }

Returns how many frames an active item's CollectibleEffect should last.
___
### Name {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string Name  {: .copyable aria-label='Variables' }

Returns the item's name.

???- warning "Warning"
    In Repentance, returns "#[ITEM_NAME]" rather than the item's ingame name. (i.e. The Sad Onion will return #THE_SAD_ONION_NAME)
___
### Passive·Cache {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean PassiveCache  {: .copyable aria-label='Variables' }

Whether or not a cache evaluation is called when the item is picked up. (used in item's like "Mom's Box")
___
### Persistent·Effect {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### boolean PersistentEffect  {: .copyable aria-label='Variables' }

Returns whether or not an active item's CollectibleEffect should persist between rooms. Any item without this set will return ``:::lua false``.
___
### Quality {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int Quality  {: .copyable aria-label='Variables' }

Returns the item's quality. Possible values are 0, 1, 2, 3, 4.
___
### Shop·Price {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int ShopPrice  {: .copyable aria-label='Variables' }

Returns the cost of the item at a shop. Returns ``:::lua 15`` if the item has no defined price in [items.xml](xml/items.md).
___
### Special {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean Special  {: .copyable aria-label='Variables' }

For the special collectible reroll system. (not applicable in Repentance)
___
### Tags {: aria-label='Variables' }
[ ](#){: .reporplus .tooltip .badge }
#### int Tags  {: .copyable aria-label='Variables' }

Returns the tags of the item.
___
### Type {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [ItemType](enums/ItemType.md) Type  {: .copyable aria-label='Variables' }

The item's [ItemType](enums/ItemType.md).
___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "HasTags",
    "signature": "boolean HasTags ( int Tags ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "IsAvailable",
    "signature": "boolean IsAvailable ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "IsCollectible",
    "signature": "boolean IsCollectible ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "IsNull",
    "signature": "boolean IsNull ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "IsTrinket",
    "signature": "boolean IsTrinket ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "AchievementID",
    "signature": "int AchievementID  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "AddBlackHearts",
    "signature": "int AddBlackHearts  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "AddBombs",
    "signature": "int AddBombs  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "AddCoins",
    "signature": "int AddCoins  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "AddCostumeOnPickup",
    "signature": "boolean AddCostumeOnPickup  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "AddHearts",
    "signature": "int AddHearts  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "AddKeys",
    "signature": "int AddKeys  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "AddMaxHearts",
    "signature": "int AddMaxHearts  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "AddSoulHearts",
    "signature": "int AddSoulHearts  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "CacheFlags",
    "signature": "int CacheFlags  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m016",
    "name": "ChargeType",
    "signature": "int ChargeType  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m017",
    "name": "ClearEffectsOnRemove",
    "signature": "boolean ClearEffectsOnRemove  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m018",
    "name": "Costume",
    "signature": "const [Costume](ItemConfig_Costume.md) Costume {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m019",
    "name": "CraftingQuality",
    "signature": "int CraftingQuality  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m020",
    "name": "Description",
    "signature": "string Description  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m021",
    "name": "DevilPrice",
    "signature": "int DevilPrice  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m022",
    "name": "Discharged",
    "signature": "boolean Discharged  {: .copyable aria-label='Variables' }",
    "description": "This attribute got removed with Repentance."
  },
  {
    "method_id": "m023",
    "name": "GfxFileName",
    "signature": "string GfxFileName  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m024",
    "name": "Hidden",
    "signature": "boolean Hidden  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m025",
    "name": "ID",
    "signature": "int ID  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m026",
    "name": "InitCharge",
    "signature": "int InitCharge  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m027",
    "name": "MaxCharges",
    "signature": "int MaxCharges  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m028",
    "name": "MaxCooldown",
    "signature": "int MaxCooldown  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m029",
    "name": "Name",
    "signature": "string Name  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m030",
    "name": "PassiveCache",
    "signature": "boolean PassiveCache  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m031",
    "name": "PersistentEffect",
    "signature": "boolean PersistentEffect  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m032",
    "name": "Quality",
    "signature": "int Quality  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m033",
    "name": "ShopPrice",
    "signature": "int ShopPrice  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m034",
    "name": "Special",
    "signature": "boolean Special  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m035",
    "name": "Tags",
    "signature": "int Tags  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m036",
    "name": "Type",
    "signature": "[ItemType](enums/ItemType.md) Type  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "Represents configuration data for a single item (collectible, trinket, or null item), providing access to its properties such as costs, hearts added, tags, quality, and unlock status.",
    "use_cases": [
      "Retrieving item stats for display",
      "Checking if an item is available in the current run",
      "Determining item type and characteristics",
      "Accessing item cost for shops/devil deals",
      "Reading item tags for transformation checks"
    ],
    "key_methods": [
      "HasTags",
      "IsAvailable",
      "ID",
      "Name",
      "Type"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "Checks whether the item has a specific tag or set of tags, typically used for transformation or category filtering.",
      "use_cases": [
        "Verifying if an item contributes to a transformation (e.g., Bob transformation)",
        "Filtering items by tag for custom pools or logic"
      ],
      "key_methods": ["HasTags", "Tags"]
    },
    {
      "method_id": "m002",
      "summary": "Returns true if the item is unlocked and not blocked by tags, otherwise false.",
      "use_cases": [
        "Determining if an item can appear in the current run",
        "Filtering item lists to only available items"
      ],
      "key_methods": ["IsAvailable", "AchievementID", "Hidden"]
    },
    {
      "method_id": "m003",
      "summary": "Returns true if the item is a collectible (active or passive).",
      "use_cases": [
        "Type-checking before applying collectible-specific logic",
        "Differentiating between collectibles, trinkets, and null items"
      ],
      "key_methods": ["IsCollectible", "IsTrinket", "IsNull", "Type"]
    },
    {
      "method_id": "m004",
      "summary": "Returns true if the item is a null item (i.e., not a valid collectible or trinket).",
      "use_cases": [
        "Validating that an obtained ItemConfigItem reference corresponds to a real item"
      ],
      "key_methods": ["IsNull", "IsCollectible", "IsTrinket"]
    },
    {
      "method_id": "m005",
      "summary": "Returns true if the item is a trinket.",
      "use_cases": [
        "Distinguishing trinkets from collectibles when handling item data",
        "Building trinket‑only UI or logic"
      ],
      "key_methods": ["IsTrinket", "IsCollectible", "IsNull"]
    },
    {
      "method_id": "m006",
      "summary": "Returns the achievement ID required to unlock the item, or -1 if unlocked by default.",
      "use_cases": [
        "Checking which achievement unlocks an item",
        "Displaying unlock requirements in custom menus"
      ],
      "key_methods": ["AchievementID", "IsAvailable"]
    },
    {
      "method_id": "m007",
      "summary": "Returns the number of black hearts (half‑heart units) the item grants on pickup.",
      "use_cases": [
        "Calculating total health gain from an item",
        "Balancing custom items or showing pickup previews"
      ],
      "key_methods": ["AddBlackHearts", "AddSoulHearts", "AddHearts", "AddMaxHearts"]
    },
    {
      "method_id": "m008",
      "summary": "Returns the number of bombs the item adds to the player.",
      "use_cases": [
        "Determining bomb‑related bonuses",
        "Simulating item pickup effects"
      ],
      "key_methods": ["AddBombs", "AddKeys", "AddCoins"]
    },
    {
      "method_id": "m009",
      "summary": "Returns the number of coins the item adds to the player.",
      "use_cases": [
        "Evaluating coin gain from an item",
        "Custom shop or economy modding"
      ],
      "key_methods": ["AddCoins", "AddBombs", "AddKeys"]
    },
    {
      "method_id": "m010",
      "summary": "Indicates whether the item adds its associated costume when picked up.",
      "use_cases": [
        "Controlling visual appearance changes",
        "Preventing costume application in certain mods"
      ],
      "key_methods": ["AddCostumeOnPickup", "Costume"]
    },
    {
      "method_id": "m011",
      "summary": "Returns the number of red hearts (half‑heart units) the item heals.",
      "use_cases": [
        "Calculating health restoration from an item",
        "Item stat display for mods"
      ],
      "key_methods": ["AddHearts", "AddSoulHearts", "AddBlackHearts", "AddMaxHearts"]
    },
    {
      "method_id": "m012",
      "summary": "Returns the number of keys the item adds to the player.",
      "use_cases": [
        "Determining resource gain from items",
        "Custom pickup effects"
      ],
      "key_methods": ["AddKeys", "AddBombs", "AddCoins"]
    },
    {
      "method_id": "m013",
      "summary": "Returns the number of empty heart containers (half‑heart units) the item grants, increasing maximum health.",
      "use_cases": [
        "Calculating max‑HP changes from an item",
        "Previewing health capacity before pickup"
      ],
      "key_methods": ["AddMaxHearts", "AddHearts", "AddSoulHearts"]
    },
    {
      "method_id": "m014",
      "summary": "Returns the number of soul hearts (half‑heart units) the item adds to the player.",
      "use_cases": [
        "Checking soul heart gains from an item",
        "Adjusting item balance"
      ],
      "key_methods": ["AddSoulHearts", "AddBlackHearts", "AddHearts"]
    },
    {
      "method_id": "m015",
      "summary": "Returns the CacheFlag bitmask that specifies which player stats the item modifies.",
      "use_cases": [
        "Understanding stat‑change triggers for passive items",
        "Building systems that react to cache evaluations"
      ],
      "key_methods": ["CacheFlags", "PassiveCache"]
    },
    {
      "method_id": "m016",
      "summary": "Returns the charge type (0: Normal, 1: Timed, 2: Special) for active items.",
      "use_cases": [
        "Classifying active item behavior",
        "Implementing custom charge mechanics"
      ],
      "key_methods": ["ChargeType", "MaxCharges", "InitCharge"]
    },
    {
      "method_id": "m017",
      "summary": "Returns whether the item's effects should be cleared when the item is removed from the player.",
      "use_cases": [
        "Handling item removal logic in mods",
        "Understanding persistent vs temporary effects"
      ],
      "key_methods": ["ClearEffectsOnRemove", "PersistentEffect"]
    },
    {
      "method_id": "m018",
      "summary": "Returns the Costume object that the item provides, describing its visual appearance changes.",
      "use_cases": [
        "Retrieving costume data for custom rendering",
        "Checking if an item has a visual effect"
      ],
      "key_methods": ["Costume", "AddCostumeOnPickup"]
    },
    {
      "method_id": "m019",
      "summary": "Returns the quality used for the Bag of Crafting algorithm; -1 means the item cannot be crafted.",
      "use_cases": [
        "Adjusting crafting recipes",
        "Displaying crafting potential in UI"
      ],
      "key_methods": ["CraftingQuality", "Quality"]
    },
    {
      "method_id": "m020",
      "summary": "Returns the item description string, which in Repentance is a placeholder key (e.g., '#THE_SAD_ONION_DESCRIPTION').",
      "use_cases": [
        "Retrieving description for custom mod tooltips",
        "Localization or string replacement"
      ],
      "key_methods": ["Description", "Name"]
    },
    {
      "method_id": "m021",
      "summary": "Returns the heart cost (full red heart units) for purchasing the item in a devil deal.",
      "use_cases": [
        "Calculating devil deal prices",
        "Displaying cost previews in custom shops"
      ],
      "key_methods": ["DevilPrice", "ShopPrice"]
    },
    {
      "method_id": "m022",
      "summary": "Removed attribute from Repentance; previously indicated a discharged state. No functional use in current version.",
      "use_cases": [],
      "key_methods": ["Discharged"]
    },
    {
      "method_id": "m023",
      "summary": "Returns the file path to the item's graphics file (GFX).",
      "use_cases": [
        "Loading custom sprites for mods",
        "Referencing item animations"
      ],
      "key_methods": ["GfxFileName", "ID"]
    },
    {
      "method_id": "m024",
      "summary": "Returns true if the item should not appear in the Death Certificate area.",
      "use_cases": [
        "Item pool manipulation",
        "Hiding certain items from Death Certificate in mods"
      ],
      "key_methods": ["Hidden", "IsAvailable"]
    },
    {
      "method_id": "m025",
      "summary": "Returns the numeric CollectibleType/TrinketType ID of the item.",
      "use_cases": [
        "Using the ID for item spawning or logic branching",
        "Mapping ID to item name or data"
      ],
      "key_methods": ["ID", "Name", "Type"]
    },
    {
      "method_id": "m026",
      "summary": "Returns the initial charge amount an active item has when first picked up; -1 means fully charged.",
      "use_cases": [
        "Setting up active item charge on acquisition",
        "Balancing new active items"
      ],
      "key_methods": ["InitCharge", "MaxCharges", "ChargeType"]
    },
    {
      "method_id": "m027",
      "summary": "Returns the maximum charge capacity of an active item.",
      "use_cases": [
        "Charge bar calculations",
        "Active item balance testing"
      ],
      "key_methods": ["MaxCharges", "InitCharge", "ChargeType"]
    },
    {
      "method_id": "m028",
      "summary": "Returns the maximum cooldown (in frames) for an active item's effect.",
      "use_cases": [
        "Understanding active item duration",
        "Timing custom effects"
      ],
      "key_methods": ["MaxCooldown", "MaxCharges"]
    },
    {
      "method_id": "m029",
      "summary": "Returns the item name string, which in Repentance is a placeholder key (e.g., '#THE_SAD_ONION_NAME').",
      "use_cases": [
        "Displaying item names in custom UI",
        "Localization or string replacement"
      ],
      "key_methods": ["Name", "Description", "ID"]
    },
    {
      "method_id": "m030",
      "summary": "Indicates whether a cache evaluation is triggered when the item is picked up (relevant for items like Mom's Box).",
      "use_cases": [
        "Modifying passive item behavior",
        "Debugging stat update triggers"
      ],
      "key_methods": ["PassiveCache", "CacheFlags"]
    },
    {
      "method_id": "m031",
      "summary": "Returns true if an active item's effect persists between rooms.",
      "use_cases": [
        "Designing items with room‑persistent effects",
        "Checking effect lifespan"
      ],
      "key_methods": ["PersistentEffect", "ClearEffectsOnRemove"]
    },
    {
      "method_id": "m032",
      "summary": "Returns the item quality value (0 to 4), representing general power level.",
      "use_cases": [
        "Evaluating item strength",
        "Quality‑based item sorting or filtering"
      ],
      "key_methods": ["Quality", "CraftingQuality"]
    },
    {
      "method_id": "m033",
      "summary": "Returns the shop price (in coins) for the item; defaults to 15 if not defined.",
      "use_cases": [
        "Calculating shop purchase costs",
        "Custom economy modding"
      ],
      "key_methods": ["ShopPrice", "DevilPrice"]
    },
    {
      "method_id": "m034",
      "summary": "Boolean flag for the deprecated special item reroll system; not used in Repentance.",
      "use_cases": [],
      "key_methods": ["Special"]
    },
    {
      "method_id": "m035",
      "summary": "Returns the raw integer bitmask of tags assigned to the item.",
      "use_cases": [
        "Direct bitwise tag checks",
        "Storing or comparing tag data"
      ],
      "key_methods": ["Tags", "HasTags"]
    },
    {
      "method_id": "m036",
      "summary": "Returns the ItemType enum value (e.g., ACTIVE, PASSIVE, FAMILIAR, TRINKET) of the item.",
      "use_cases": [
        "Categorizing items by type",
        "Switching on item type for logic"
      ],
      "key_methods": ["Type", "ID", "IsCollectible", "IsTrinket", "IsNull"]
    }
  ]
}
```
