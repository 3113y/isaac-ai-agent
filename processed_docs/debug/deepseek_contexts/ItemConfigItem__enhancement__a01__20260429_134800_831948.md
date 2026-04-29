# DeepSeek Context

- class: ItemConfigItem
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:48:00.832002

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

```
