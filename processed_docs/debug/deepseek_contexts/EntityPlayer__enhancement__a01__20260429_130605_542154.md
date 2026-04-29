# DeepSeek Context

- class: EntityPlayer
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:06:05.542192

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

类名：EntityPlayer

原始 md 文档（该类完整文档，可能已截断）：
# Class "EntityPlayer"

???+ info
    你可以通过以下函数获取此类：

    * [Entity.ToPlayer()](Entity.md#toplayer)
    * [EntityFamiliar.Player](EntityFamiliar.md#player)
    * [EntityPlayer.GetMainTwin()](EntityPlayer.md#getmaintwin)
    * [EntityPlayer.GetOtherTwin()](EntityPlayer.md#getothertwin)
    * [EntityPlayer.GetSubPlayer()](EntityPlayer.md#getsubplayer)
    * [Game.GetNearestPlayer()](Game.md#getnearestplayer)
    * [Game.GetPlayer()](Game.md#getplayer)
    * [Game.GetRandomPlayer()](Game.md#getrandomplayer)
    * [Isaac.GetPlayer()](Isaac.md#getplayer)

    ???+ example "Example Code"
        `local player = Isaac.GetPlayer()`

## Class Diagram
--8<-- "docs/snippets/EntityClassDiagram.md"
## Functions
### Add·Black·Hearts () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddBlackHearts ( int BlackHearts ) {: .copyable aria-label='Functions' }

给玩家添加黑心。1个单位是半颗心。用负数移除它们。

???- example "Example Code"

    This code adds 1 full black heart to the player.

    ```lua
    Isaac.GetPlayer():AddBlackHearts(2)
    ```

___
### Add·Blood·Charge () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddBloodCharge ( int Amount ) {: .copyable aria-label='Functions' }

给玩家添加血量充能。血量充能在除堕化伯大妮以外的角色上没有任何作用。

___
### Add·Blue·Flies () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### [Entity](Entity.md) AddBlueFlies ( int Amount, [Vector](Vector.md) Position, [Entity](Entity.md) Target ) {: .copyable aria-label='Functions' }
???- info "Amount"

    饰品**鱼尾**将始终将此函数添加的苍蝇数量加倍。

___
### Add·Blue·Spider () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### [Entity](Entity.md) AddBlueSpider ( [Vector](Vector.md) Position ) {: .copyable aria-label='Functions' }

???- example "Example Code"

    This code spawns 3 blue spiders at the player's position.

    ```lua
    local player = Isaac.GetPlayer()
    for _ = 1, 3 do
	player:AddBlueSpider(player.Position)
    end
    ```

___
### Add·Bombs () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddBombs ( int Amount ) {: .copyable aria-label='Functions' }

给玩家添加炸弹。用负数移除它们。

???- example "Example Code"

    This code removes 1 bomb from the player.

    ```lua
    Isaac.GetPlayer():AddBombs(-1)
    ```

___
### Add·Bone·Hearts () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddBoneHearts ( int Hearts ) {: .copyable aria-label='Functions' }

给玩家添加骨心。1个单位是单颗骨心。用负数移除它们。

???- example "Example Code"

    This code adds 1 bone heart to the player.

    ```lua
    Isaac.GetPlayer():AddBoneHearts(1)
    ```

___
### Add·Broken·Hearts () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddBrokenHearts ( int BrokenHearts ) {: .copyable aria-label='Functions' }

给玩家添加碎心。1个单位是单颗碎心。用负数移除它们。

???- example "Example Code"

    This code adds 1 broken heart to the player, then takes it away.

    ```lua
    Isaac.GetPlayer():AddBrokenHearts(1)
    Isaac.GetPlayer():AddBrokenHearts(-1)
    ```
___
### Add·Cache·Flags () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddCacheFlags ( [CacheFlag](enums/CacheFlag.md) CacheFlag ) {: .copyable aria-label='Functions' }

在下一次缓存重新计算中，将重新计算提供的缓存标志。

???- example "Example Code"

    This code will add several cacheflags.

    ```lua
    Isaac.GetPlayer():AddCacheFlags(CacheFlag.CACHE_DAMAGE | CacheFlag.CACHE_FIREDELAY | CacheFlag.CACHE_LUCK)
    ```
___
### Add·Card () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddCard ( [Card](enums/Card.md) ID ) {: .copyable aria-label='Functions' }

___
### Add·Coins () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddCoins ( int Amount ) {: .copyable aria-label='Functions' }

给玩家添加金币。用负数移除它们。

???- example "Example Code"

    This code adds 1 coin to the player.

    ```lua
    Isaac.GetPlayer():AddCoins(1)
    ```

___
### Add·Collectible () {: aria-label='Functions' }
[ ](#){: .rep .tooltip .badge }
#### void AddCollectible ( [CollectibleType](enums/CollectibleType.md) Type, int Charge = 0, boolean FirstTimePickingUp = true, [ActiveSlot](enums/ActiveSlot.md) Slot = ActiveSlot.SLOT_PRIMARY, int VarData = 0) {: .copyable aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### void AddCollectible ( [CollectibleType](enums/CollectibleType.md) Type, int Charge = 0, boolean FirstTimePickingUp = true, [ActiveSlot](enums/ActiveSlot.md) Slot = ActiveSlot.SLOT_PRIMARY, int VarData = 0, [ItemPoolType](enums/ItemPoolType.md) PoolType ) {: .copyable aria-label='Functions' }


设置 **FirstTimePickingUp** 为false 将不会添加物品的消耗品（钥匙、炸弹等），并且不会计入套装。

- Slot 0 是默认值 (normal active item)
- Slot 1 是 Schoolbag 使用的
- Slot 2 是用于口袋主动物品的

???- note "Notes"

	Slot 2 不能被用于开始时没有口袋主动物品的角色

VarData is used for the storage of a persistent context-sensitive value

???- note "Notes"

    这是一个使用 VarData 的所有物品的列表：

    - 魂火罐: 魂火会在下一次使用时生成 (最大12)
	- 无限骰, 空白卡, 透明符文, 安慰剂: 当前最大充能 (任何大于0的值)
	- Hold: 存储的便便
	    - 便便类型:
	    - [0] 无
	    - [1] 普通
	    - [2] 苍蝇
	    - [3] 火焰
	    - [4] 石化
	    - [5] 有毒
	    - [6] 黑色
	    - [7] 神圣
	    - [8] X-Lax
	    - [9] Fart
	    - [10] Bomb
	    - [11] Explosive Diarrhea
	    - [12+] Empty

___
### Add·Controls·Cooldown () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddControlsCooldown ( int Cooldown ) {: .copyable aria-label='Functions' }

___
### Add·Costume () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddCostume ( [ItemConfigItem](ItemConfig_Item.md) Item, boolean ItemStateOnly ) {: .copyable aria-label='Functions' }

___
### Add·Curse·Mist·Effect () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddCurseMistEffect ( ) {: .copyable aria-label='Functions' }

___
### Add·Dead·Eye·Charge () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddDeadEyeCharge ( ) {: .copyable aria-label='Functions' }

___
### Add·Dollar·Bill·Effect () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddDollarBillEffect ( ) {: .copyable aria-label='Functions' }

___
### Add·Eternal·Hearts () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddEternalHearts ( int EternalHearts ) {: .copyable aria-label='Functions' }

给玩家添加永恒之心。1个单位是半颗心。用负数移除它们。

（注意，当你拥有超过一个时，永恒之心会自动变为完整的心。）

???- example "Example Code"

    This code adds 1 eternal heart to the player.

    ```lua
    Isaac.GetPlayer():AddEternalHearts(1)
    ```

___
### Add·Friendly·Dip () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddFriendlyDip ( int Subtype, [Vector](Vector.md) Position ) {: .copyable aria-label='Functions' }

???- note "Dip Subtypes"

    ```lua
    0: normal
    1: red
    2: corny
    3: golden
    4: rainbow
    5: black
    6: holy
    12: stone
    13: flaming
    14: poison
    20: brownie
    ```
___
### Add·Giga·Bombs () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddGigaBombs ( int GigaBombs ) {: .copyable aria-label='Functions' }

???- note "Notes"

    巨型炸弹不会增加炸弹计数，请确保提前增加炸弹数量！
	你不能添加超过玩家当前炸弹数量的巨型炸弹。

___
### Add·Golden·Bomb () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddGoldenBomb ( ) {: .copyable aria-label='Functions' }

___
### Add·Golden·Hearts () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddGoldenHearts ( int Hearts ) {: .copyable aria-label='Functions' }

给玩家添加金心。1个单位是单颗金心。用负数移除它们。

???- example "Example Code"

    This code adds 1 golden heart to the player.

    ```lua
    Isaac.GetPlayer():AddGoldenHearts(1)
    ```

___
### Add·Golden·Key () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddGoldenKey ( ) {: .copyable aria-label='Functions' }

___
### Add·Hearts () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddHearts ( int Hearts ) {: .copyable aria-label='Functions' }

给玩家添加红心。如果有空的心容器，则添加红心。1个单位是半颗心。用负数移除生命值。

???- example "Example Code"

    This code adds 1 full red heart to the player.

    ```lua
    Isaac.GetPlayer():AddHearts(2)
    ```

___
### Add·Item·Wisp () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### [EntityFamiliar](EntityFamiliar.md) AddItemWisp ( [CollectibleType](enums/CollectibleType.md) Collectible, [Vector](Vector.md) Position, boolean AdjustOrbitLayer = false ) {: .copyable aria-label='Functions' }

___
### Add·Jar·Flies () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddJarFlies ( int Flies ) {: .copyable aria-label='Functions' }

___
### Add·Jar·Hearts () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddJarHearts ( int Hearts ) {: .copyable aria-label='Functions' }

___
### Add·Keys () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddKeys ( int Amount ) {: .copyable aria-label='Functions' }

给玩家添加钥匙。用负数移除它们。

???- example "Example Code"

    This code adds 1 key to the player.

    ```lua
    Isaac.GetPlayer():AddKeys(1)
    ```

___
### Add·Max·Hearts () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddMaxHearts ( int MaxHearts, boolean IgnoreKeeper ) {: .copyable aria-label='Functions' }

给玩家添加心容器。2个单位是一个完整的心容器。用负数移除它们。

???- note "Notes"

    可以添加半颗心容器到玩家身上。这将显示为常规心容器，但只能填充一半。

???- example "Example Code"

    This code adds 1 heart container to the player.

    ```lua
    Isaac.GetPlayer():AddMaxHearts(2, true)
    ```


???+ bug "Bugs"

    对店长无效。IgnoreKeeper 参数似乎无法按预期工作。

    最大心容器可以添加或移除到店长身上，而不管这个布尔值是什么。

    如果店长拥有贪婪的胃袋，而这个布尔值被设置为false，则无法添加最大心容器到店长身上，但可以正常移除。

    如果店长拥有贪婪的胃袋，而这个布尔值被设置为true，则可以正常添加或移除最大心容器到店长身上。

___
### Add·Minisaac () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### [EntityFamiliar](EntityFamiliar.md) AddMinisaac ( [Vector](Vector.md) Position, boolean PlayAnim = true ) {: .copyable aria-label='Functions' }

___
### Add·Null·Costume () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddNullCostume ( [NullItemID](enums/NullItemID.md) NullId ) {: .copyable aria-label='Functions' }

___
### Add·Pill () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddPill ( [PillColor](enums/PillColor.md) Pill ) {: .copyable aria-label='Functions' }

___
### Add·Player·Form·Costume () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddPlayerFormCostume ( [PlayerForm](enums/PlayerForm.md) Form ) {: .copyable aria-label='Functions' }

添加给定变身的服装。

___
### Add·Poop·Mana () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddPoopMana ( int Num ) {: .copyable aria-label='Functions' }

添加（或移除）粪便消耗品。

___
### Add·Pretty·Fly () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddPrettyFly ( ) {: .copyable aria-label='Functions' }

___
### Add·Rotten·Hearts () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddRottenHearts ( int RottenHearts ) {: .copyable aria-label='Functions' }

添加腐烂的心。1个单位是半颗心。用负数移除腐烂的心。

???- example "Example Code"

    This code adds 1 full rotten heart to the player.

    ```lua
    Isaac.GetPlayer():AddRottenHearts(2)
    ```

___
### Add·Soul·Charge () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddSoulCharge ( int Amount ) {: .copyable aria-label='Functions' }

添加灵魂充能到玩家身上。灵魂充能对除了伯大妮以外的角色没有任何作用。

___
### Add·Soul·Hearts () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddSoulHearts ( int SoulHearts ) {: .copyable aria-label='Functions' }

添加魂心到玩家。1个单位是半颗心。用负数移除它们。

???- example "Example Code"

    This code adds 1 full soul heart to the player.

    ```lua
    Isaac.GetPlayer():AddSoulHearts(2)
    ```

___
### Add·Swarm·Fly·Orbital () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### [EntityFamiliar](EntityFamiliar.md) AddSwarmFlyOrbital ( [Vector](Vector.md) Position ) {: .copyable aria-label='Functions' }

___
### Add·Trinket () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AddTrinket ( [TrinketType](enums/TrinketType.md) Type, boolean FirstTimePickingUp = true ) {: .copyable aria-label='Functions' }

- 如果玩家没有任何空的饰品槽，这个函数将不做任何事情。

- 如果玩家有一个空的饰品槽但已经有一个饰品，新饰品将进入第一个槽，现有饰品将被推回到第二个槽。

- 如果提供的参数为0或其他无效的饰品ID，游戏将崩溃。

- 将**FirstTimePickingUp**设置为false将不会为该物品生成或添加拾取物，也不会导致其计入变身。

???- example "Example Code"

    This code adds the golden variant of the Swallowed Penny trinket to the player.

    ```lua
    Isaac.GetPlayer():AddTrinket(TrinketType.TRINKET_SWALLOWED_PENNY | TrinketType.TRINKET_GOLDEN_FLAG)
    ```

___
### Add·Wisp () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### [EntityFamiliar](EntityFamiliar.md) AddWisp ( [CollectibleType](enums/CollectibleType.md) Collectible, [Vector](Vector.md) Position, boolean AdjustOrbitLayer = false, boolean DontUpdate = false ) {: .copyable aria-label='Functions' }

魂火的类型可以通过Collectible来定义。如果ID与具有特殊魂火的主动物品不对应，则默认为常规蓝色魂火。

要访问特殊魂火变体，例如Delirious形式，您需要将`65536` (1 << 16)添加到ID。例如：Delirious Monstro的`id = s14`，因此魂火的ID为`65550`。

___
### Animate·Appear () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AnimateAppear ( ) {: .copyable aria-label='Functions' }
播放在关卡开始时通常播放的动画。
___
### Animate·Card () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AnimateCard ( [Card](enums/Card.md) ID, string AnimName = "Pickup" ) {: .copyable aria-label='Functions' }

___
### Animate·Collectible () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AnimateCollectible ( [CollectibleType](enums/CollectibleType.md) Collectible, string AnimName = "Pickup", string SpriteAnimName = "PlayerPickupSparkle" ) {: .copyable aria-label='Functions' }

`AnimName` 指 `001.000_player.anm2` 中的动画名称（例如 `Pickup` 或 `UseItem`）。 `SpriteAnimName` 指 `005.100_collectible.anm2` 中的动画名称（例如 `PlayerPickup` 或 `PlayerPickupSparkle`）。

___
### Animate·Happy () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AnimateHappy ( ) {: .copyable aria-label='Functions' }

播放高兴动画，当服用正面药丸时播放。

???- example "Example Code"

    This code plays the happy animation.

    ```lua
    Isaac.GetPlayer():AnimateHappy()
    ```

### Animate·Light·Travel () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AnimateLightTravel ( ) {: .copyable aria-label='Functions' }

播放在上升时进入光柱或进入大教堂时播放的动画。

???- example "Example Code"

	Plays the animation.

	```lua
	Isaac.GetPlayer():AnimateLightTravel()
	```

___
### Animate·Pickup () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AnimatePickup ( [Sprite](Sprite.md) sprite, boolean HideShadow = false, string AnimName = "Pickup" ) {: .copyable aria-label='Functions' }

播放拾取动画，使用任何提供的Sprite对象

HideShadow通常在渲染具有自定义阴影层的精灵时设置为true

___
### Animate·Pill () {: aria-label='Functions' }
[ ](#){: .reporplus .tooltip .badge }
#### void AnimatePill ( [PillColor](enums/PillColor.md) Pill, string AnimName = "Pickup" ) {: .copyable aria-label='Functions' }

___
### Animate·Pitfall·In () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AnimatePitfallIn ( ) {: .copyable aria-label='Functions' }

造成1/2心的伤害并播放掉入陷阱的动画。

___
### Animate·Pitfall·Out () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AnimatePitfallOut ( ) {: .copyable aria-label='Functions' }

跳出陷阱的动画。

___
### Animate·Sad () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AnimateSad ( ) {: .copyable aria-label='Functions' }

播放悲伤动画，当服用负面药丸时播放。

???- example "Example Code"

    Plays the sad animation.

	```lua
	Isaac.GetPlayer():AnimateSad()
	```
___
### Animate·Teleport () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AnimateTeleport ( boolean Up ) {: .copyable aria-label='Functions' }

当传送到另一个房间时播放的动画。

___
### Animate·Trapdoor () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .ba

[TRUNCATED: 原文过长，已截断以适配上下文窗口]

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "AddBlackHearts",
    "signature": "void AddBlackHearts ( int BlackHearts ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "AddBloodCharge",
    "signature": "void AddBloodCharge ( int Amount ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "AddBlueFlies",
    "signature": "[Entity](Entity.md) AddBlueFlies ( int Amount, [Vector](Vector.md) Position, [Entity](Entity.md) Target ) {: .copyable aria-label='Functions' }",
    "description": "???- info \"Amount\""
  },
  {
    "method_id": "m004",
    "name": "AddBlueSpider",
    "signature": "[Entity](Entity.md) AddBlueSpider ( [Vector](Vector.md) Position ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "AddBombs",
    "signature": "void AddBombs ( int Amount ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "AddBoneHearts",
    "signature": "void AddBoneHearts ( int Hearts ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "AddBrokenHearts",
    "signature": "void AddBrokenHearts ( int BrokenHearts ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "AddCacheFlags",
    "signature": "void AddCacheFlags ( [CacheFlag](enums/CacheFlag.md) CacheFlag ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "AddCard",
    "signature": "void AddCard ( [Card](enums/Card.md) ID ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "AddCoins",
    "signature": "void AddCoins ( int Amount ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "AddCollectible",
    "signature": "void AddCollectible ( [CollectibleType](enums/CollectibleType.md) Type, int Charge = 0, boolean FirstTimePickingUp = true, [ActiveSlot](enums/ActiveSlot.md) Slot = ActiveSlot.SLOT_PRIMARY, int VarData = 0) {: .copyable aria-label='Functions' }",
    "description": "[ ](#){: .repplus .tooltip .badge }"
  },
  {
    "method_id": "m012",
    "name": "void AddCollectible ( [CollectibleType](enums/CollectibleType.md) Type, int Charge = 0, boolean FirstTimePickingUp = true, [ActiveSlot](enums/ActiveSlot.md) Slot = ActiveSlot.SLOT_PRIMARY, int VarData = 0, [ItemPoolType](enums/ItemPoolType.md) PoolType )",
    "signature": "void AddControlsCooldown ( int Cooldown ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "AddCostume",
    "signature": "void AddCostume ( [ItemConfigItem](ItemConfig_Item.md) Item, boolean ItemStateOnly ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "AddCurseMistEffect",
    "signature": "void AddCurseMistEffect ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "AddDeadEyeCharge",
    "signature": "void AddDeadEyeCharge ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m016",
    "name": "AddDollarBillEffect",
    "signature": "void AddDollarBillEffect ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m017",
    "name": "AddEternalHearts",
    "signature": "void AddEternalHearts ( int EternalHearts ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m018",
    "name": "AddFriendlyDip",
    "signature": "void AddFriendlyDip ( int Subtype, [Vector](Vector.md) Position ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m019",
    "name": "AddGigaBombs",
    "signature": "void AddGigaBombs ( int GigaBombs ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m020",
    "name": "AddGoldenBomb",
    "signature": "void AddGoldenBomb ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m021",
    "name": "AddGoldenHearts",
    "signature": "void AddGoldenHearts ( int Hearts ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m022",
    "name": "AddGoldenKey",
    "signature": "void AddGoldenKey ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m023",
    "name": "AddHearts",
    "signature": "void AddHearts ( int Hearts ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m024",
    "name": "AddItemWisp",
    "signature": "[EntityFamiliar](EntityFamiliar.md) AddItemWisp ( [CollectibleType](enums/CollectibleType.md) Collectible, [Vector](Vector.md) Position, boolean AdjustOrbitLayer = false ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m025",
    "name": "AddJarFlies",
    "signature": "void AddJarFlies ( int Flies ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m026",
    "name": "AddJarHearts",
    "signature": "void AddJarHearts ( int Hearts ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m027",
    "name": "AddKeys",
    "signature": "void AddKeys ( int Amount ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m028",
    "name": "AddMaxHearts",
    "signature": "void AddMaxHearts ( int MaxHearts, boolean IgnoreKeeper ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m029",
    "name": "AddMinisaac",
    "signature": "[EntityFamiliar](EntityFamiliar.md) AddMinisaac ( [Vector](Vector.md) Position, boolean PlayAnim = true ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m030",
    "name": "AddNullCostume",
    "signature": "void AddNullCostume ( [NullItemID](enums/NullItemID.md) NullId ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m031",
    "name": "AddPill",
    "signature": "void AddPill ( [PillColor](enums/PillColor.md) Pill ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m032",
    "name": "AddPlayerFormCostume",
    "signature": "void AddPlayerFormCostume ( [PlayerForm](enums/PlayerForm.md) Form ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m033",
    "name": "AddPoopMana",
    "signature": "void AddPoopMana ( int Num ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m034",
    "name": "AddPrettyFly",
    "signature": "void AddPrettyFly ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m035",
    "name": "AddRottenHearts",
    "signature": "void AddRottenHearts ( int RottenHearts ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m036",
    "name": "AddSoulCharge",
    "signature": "void AddSoulCharge ( int Amount ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m037",
    "name": "AddSoulHearts",
    "signature": "void AddSoulHearts ( int SoulHearts ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m038",
    "name": "AddSwarmFlyOrbital",
    "signature": "[EntityFamiliar](EntityFamiliar.md) AddSwarmFlyOrbital ( [Vector](Vector.md) Position ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m039",
    "name": "AddTrinket",
    "signature": "void AddTrinket ( [TrinketType](enums/TrinketType.md) Type, boolean FirstTimePickingUp = true ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m040",
    "name": "AddWisp",
    "signature": "[EntityFamiliar](EntityFamiliar.md) AddWisp ( [CollectibleType](enums/CollectibleType.md) Collectible, [Vector](Vector.md) Position, boolean AdjustOrbitLayer = false, boolean DontUpdate = false ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m041",
    "name": "AnimateAppear",
    "signature": "void AnimateAppear ( ) {: .copyable aria-label='Functions' }",
    "description": "播放在关卡开始时通常播放的动画。"
  },
  {
    "method_id": "m042",
    "name": "AnimateCard",
    "signature": "void AnimateCard ( [Card](enums/Card.md) ID, string AnimName = \"Pickup\" ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m043",
    "name": "AnimateCollectible",
    "signature": "void AnimateCollectible ( [CollectibleType](enums/CollectibleType.md) Collectible, string AnimName = \"Pickup\", string SpriteAnimName = \"PlayerPickupSparkle\" ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m044",
    "name": "AnimateHappy",
    "signature": "void AnimateHappy ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m045",
    "name": "AnimateLightTravel",
    "signature": "void AnimateLightTravel ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m046",
    "name": "AnimatePickup",
    "signature": "void AnimatePickup ( [Sprite](Sprite.md) sprite, boolean HideShadow = false, string AnimName = \"Pickup\" ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m047",
    "name": "AnimatePill",
    "signature": "void AnimatePill ( [PillColor](enums/PillColor.md) Pill, string AnimName = \"Pickup\" ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m048",
    "name": "AnimatePitfallIn",
    "signature": "void AnimatePitfallIn ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m049",
    "name": "AnimatePitfallOut",
    "signature": "void AnimatePitfallOut ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m050",
    "name": "AnimateSad",
    "signature": "void AnimateSad ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m051",
    "name": "AnimateTeleport",
    "signature": "void AnimateTeleport ( boolean Up ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m052",
    "name": "AnimateTrapdoor",
    "signature": "void AnimateTrapdoor ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m053",
    "name": "AnimateTrinket",
    "signature": "void AnimateTrinket ( [TrinketType](enums/TrinketType.md) Trinket, string AnimName = \"Pickup\", string SpriteAnimName = \"PlayerPickupSparkle\" ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m054",
    "name": "AreControlsEnabled",
    "signature": "boolean AreControlsEnabled ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m055",
    "name": "AreOpposingShootDirectionsPressed",
    "signature": "boolean AreOpposingShootDirectionsPressed ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m056",
    "name": "CanAddCollectible",
    "signature": "boolean CanAddCollectible ( [CollectibleType](enums/CollectibleType.md) Type = CollectibleType.COLLECTIBLE_NULL ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m057",
    "name": "CanPickBlackHearts",
    "signature": "boolean CanPickBlackHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m058",
    "name": "CanPickBoneHearts",
    "signature": "boolean CanPickBoneHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m059",
    "name": "CanPickGoldenHearts",
    "signature": "boolean CanPickGoldenHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m060",
    "name": "CanPickRedHearts",
    "signature": "boolean CanPickRedHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m061",
    "name": "CanPickRottenHearts",
    "signature": "boolean CanPickRottenHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m062",
    "name": "CanPickSoulHearts",
    "signature": "boolean CanPickSoulHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m063",
    "name": "CanPickupItem",
    "signature": "boolean CanPickupItem ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m064",
    "name": "CanShoot",
    "signature": "boolean CanShoot ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m065",
    "name": "CanTurnHead",
    "signature": "boolean CanTurnHead ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m066",
    "name": "ChangePlayerType",
    "signature": "void ChangePlayerType ( [PlayerType](enums/PlayerType.md) PlayerType ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m067",
    "name": "CheckFamiliar",
    "signature": "void CheckFamiliar ( [FamiliarVariant](enums/FamiliarVariant.md) FamiliarVariant, int TargetCount, [RNG](RNG.md) rng, [ItemConfigItem](ItemConfig_Item.md) SourceItemConfigItem = nil, int FamiliarSubType = -1 ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m068",
    "name": "ClearCostumes",
    "signature": "void ClearCostumes ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m069",
    "name": "ClearDeadEyeCharge",
    "signature": "void ClearDeadEyeCharge ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m070",
    "name": "ClearTemporaryEffects",
    "signature": "void ClearTemporaryEffects ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m071",
    "name": "DischargeActiveItem",
    "signature": "void DischargeActiveItem ( [ActiveSlot](enums/ActiveSlot.md) ActiveSlot = ActiveSlot.SLOT_PRIMARY ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m072",
    "name": "DonateLuck",
    "signature": "void DonateLuck ( int Luck ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m073",
    "name": "DoZitEffect",
    "signature": "void DoZitEffect ( [Vector](Vector.md) Direction ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m074",
    "name": "DropPocketItem",
    "signature": "void DropPocketItem ( int PocketNum, [Vector](Vector.md) Pos ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m075",
    "name": "DropTrinket",
    "signature": "void DropTrinket ( [Vector](Vector.md) DropPos, boolean ReplaceTick ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m076",
    "name": "EvaluateItems",
    "signature": "void EvaluateItems ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m077",
    "name": "FireBomb",
    "signature": "[EntityBomb](EntityBomb.md) FireBomb ( [Vector](Vector.md) Position, [Vector](Vector.md) Velocity, Entity Source = nil ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m078",
    "name": "FireBrimstone",
    "signature": "[EntityLaser](EntityLaser.md) FireBrimstone ( [Vector](Vector.md) Direction, Entity Source = nil, float DamageMultiplier = 1 ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m079",
    "name": "FireDelayedBrimstone",
    "signature": "[EntityLaser](EntityLaser.md) FireDelayedBrimstone ( float Angle, [Entity](Entity.md) Parent ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m080",
    "name": "FireKnife",
    "signature": "[EntityKnife](EntityKnife.md) FireKnife ( [Entity](Entity.md) Parent, float RotationOffset = 0, boolean CantOverwrite = false, int SubType = 0, int Variant = 0 ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m081",
    "name": "FireTear",
    "signature": "[EntityTear](EntityTear.md) FireTear ( [Vector](Vector.md) Position, [Vector](Vector.md) Velocity, boolean CanBeEye = true, boolean NoTractorBeam = false, boolean CanTriggerStreakEnd = true, Entity Source = nil, float DamageMultiplier = 1 ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m082",
    "name": "FireTechLaser",
    "signature": "[EntityLaser](EntityLaser.md) FireTechLaser ( [Vector](Vector.md) Position, [LaserOffset](enums/LaserOffset.md) OffsetID, [Vector](Vector.md) Direction, boolean LeftEye, boolean OneHit = false, Entity Source = nil, float DamageMultiplier = 1 ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m083",
    "name": "FireTechXLaser",
    "signature": "[EntityLaser](EntityLaser.md) FireTechXLaser ( [Vector](Vector.md) Position, [Vector](Vector.md) Direction, float Radius, Entity Source = nil, float DamageMultiplier = 1 ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m084",
    "name": "FlushQueueItem",
    "signature": "boolean FlushQueueItem ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m085",
    "name": "FullCharge",
    "signature": "boolean FullCharge ( [ActiveSlot](enums/ActiveSlot.md) ActiveSlot = ActiveSlot.SLOT_PRIMARY, int Force = false ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m086",
    "name": "GetActiveCharge",
    "signature": "int GetActiveCharge ( [ActiveSlot](enums/ActiveSlot.md) ActiveSlot = ActiveSlot.SLOT_PRIMARY ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m087",
    "name": "GetActiveItem",
    "signature": "[CollectibleType](enums/CollectibleType.md) GetActiveItem ( [ActiveSlot](enums/ActiveSlot.md) ActiveSlot = ActiveSlot.SLOT_PRIMARY ) {: .copyable aria-label='Functions' data-altreturn='0' }",
    "description": ""
  },
  {
    "method_id": "m088",
    "name": "GetActiveSubCharge",
    "signature": "int GetActiveSubCharge ( [ActiveSlot](enums/ActiveSlot.md) ActiveSlot = ActiveSlot.SLOT_PRIMARY ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m089",
    "name": "GetActiveWeaponEntity",
    "signature": "[Entity](Entity.md) GetActiveWeaponEntity ( ) {: .copyable aria-label='Functions' data-altreturn='nil' }",
    "description": ""
  },
  {
    "method_id": "m090",
    "name": "GetAimDirection",
    "signature": "const [Vector](Vector.md) GetAimDirection ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m091",
    "name": "GetBabySkin",
    "signature": "[BabySubType](enums/BabySubType.md) GetBabySkin ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m092",
    "name": "GetBatteryCharge",
    "signature": "int GetBatteryCharge ( [ActiveSlot](enums/ActiveSlot.md) ActiveSlot = ActiveSlot.SLOT_PRIMARY ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m093",
    "name": "GetBlackHearts",
    "signature": "int GetBlackHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m094",
    "name": "GetBloodCharge",
    "signature": "int GetBloodCharge ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m095",
    "name": "GetBodyColor",
    "signature": "[SkinColor](enums/SkinColor.md) GetBodyColor ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m096",
    "name": "GetBombFlags",
    "signature": "int GetBombFlags ( ) {: .copyable aria-label='Functions' }",
    "description": "[ ](#){: .reporplus .tooltip .badge }"
  },
  {
    "method_id": "m097",
    "name": "int GetBombFlags ( boolean IsFetus = false )",
    "signature": "[BombVariant](enums/BombVariant.md) GetBombVariant ( [TearFlags](enums/TearFlags.md) TearFlags, boolean ForceSmallBomb ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m098",
    "name": "GetBoneHearts",
    "signature": "int GetBoneHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m099",
    "name": "GetBrokenHearts",
    "signature": "int GetBrokenHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m100",
    "name": "GetCard",
    "signature": "[Card](enums/Card.md) GetCard ( int SlotId ) {: .copyable aria-label='Functions' data-altreturn='0' }",
    "description": ""
  },
  {
    "method_id": "m101",
    "name": "GetCardRNG",
    "signature": "[RNG](RNG.md) GetCardRNG ( [Card](enums/Card.md) ID ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m102",
    "name": "GetCollectibleCount",
    "signature": "int GetCollectibleCount ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m103",
    "name": "GetCollectibleNum",
    "signature": "int GetCollectibleNum ( [CollectibleType](enums/CollectibleType.md) Type, boolean OnlyCountTrueItems = false ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m104",
    "name": "GetCollectibleRNG",
    "signature": "[RNG](RNG.md) GetCollectibleRNG ( [CollectibleType](enums/CollectibleType.md) ID ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m105",
    "name": "GetCostumeNullPos",
    "signature": "[Vector](Vector.md) GetCostumeNullPos ( string NullFrameName, boolean HeadScale, [Vector](Vector.md) Direction ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m106",
    "name": "GetDamageCooldown",
    "signature": "int GetDamageCooldown ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m107",
    "name": "GetEffectiveBloodCharge",
    "signature": "int GetEffectiveBloodCharge ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m108",
    "name": "GetEffectiveMaxHearts",
    "signature": "int GetEffectiveMaxHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m109",
    "name": "GetEffectiveSoulCharge",
    "signature": "int GetEffectiveSoulCharge ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m110",
    "name": "GetEffects",
    "signature": "[TemporaryEffects](TemporaryEffects.md) GetEffects ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m111",
    "name": "GetEternalHearts",
    "signature": "int GetEternalHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m112",
    "name": "GetExtraLives",
    "signature": "int GetExtraLives ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m113",
    "name": "GetFireDirection",
    "signature": "[Direction](enums/Direction.md) GetFireDirection ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m114",
    "name": "GetFlyingOffset",
    "signature": "[Vector](Vector.md) GetFlyingOffset ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m115",
    "name": "GetGoldenHearts",
    "signature": "int GetGoldenHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m116",
    "name": "GetGreedDonationBreakChance",
    "signature": "float GetGreedDonationBreakChance ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m117",
    "name": "GetHeadColor",
    "signature": "[SkinColor](enums/SkinColor.md) GetHeadColor ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m118",
    "name": "GetHeadDirection",
    "signature": "[Direction](enums/Direction.md) GetHeadDirection ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m119",
    "name": "GetHeartLimit",
    "signature": "int GetHeartLimit ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m120",
    "name": "GetHearts",
    "signature": "int GetHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m121",
    "name": "GetItemState",
    "signature": "[CollectibleType](enums/CollectibleType.md) GetItemState ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m122",
    "name": "GetJarFlies",
    "signature": "int GetJarFlies ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m123",
    "name": "GetJarHearts",
    "signature": "int GetJarHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m124",
    "name": "GetLaserOffset",
    "signature": "[Vector](Vector.md) GetLaserOffset ( [LaserOffset](enums/LaserOffset.md) ID, [Vector](Vector.md) Direction ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m125",
    "name": "GetLastActionTriggers",
    "signature": "int GetLastActionTriggers ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m126",
    "name": "GetLastDamageFlags",
    "signature": "int GetLastDamageFlags ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m127",
    "name": "GetLastDamageSource",
    "signature": "const [EntityRef](EntityRef.md) GetLastDamageSource ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m128",
    "name": "GetLastDirection",
    "signature": "const [Vector](Vector.md) GetLastDirection ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m129",
    "name": "GetMainTwin",
    "signature": "[EntityPlayer](EntityPlayer.md) GetMainTwin ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m130",
    "name": "GetMaxHearts",
    "signature": "int GetMaxHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m131",
    "name": "GetMaxPocketItems",
    "signature": "int GetMaxPocketItems ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m132",
    "name": "GetMaxPoopMana",
    "signature": "int GetMaxPoopMana ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m133",
    "name": "GetMaxTrinkets",
    "signature": "int GetMaxTrinkets ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m134",
    "name": "GetModelingClayEffect",
    "signature": "[CollectibleType](enums/CollectibleType.md) GetModelingClayEffect ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m135",
    "name": "GetMovementDirection",
    "signature": "[Direction](enums/Direction.md) GetMovementDirection ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m136",
    "name": "GetMovementInput",
    "signature": "const [Vector](Vector.md) GetMovementInput ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m137",
    "name": "GetMovementJoystick",
    "signature": "[Vector](Vector.md) GetMovementJoystick ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m138",
    "name": "GetMovementVector",
    "signature": "[Vector](Vector.md) GetMovementVector ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m139",
    "name": "GetMultiShotParams",
    "signature": "MultiShotParams GetMultiShotParams ( [WeaponType](enums/WeaponType.md) WeaponType = WeaponType.WEAPON_TEARS ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m140",
    "name": "GetMultiShotPositionVelocity",
    "signature": "[PosVel](PlayerTypes_PosVel.md) GetMultiShotPositionVelocity ( int LoopIndex, [WeaponType](enums/WeaponType.md) Weapon, [Vector](Vector.md) ShotDirection, float ShotSpeed, MultiShotParams params ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m141",
    "name": "GetName",
    "signature": "string GetName ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m142",
    "name": "GetNPCTarget",
    "signature": "[Entity](Entity.md) GetNPCTarget ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m143",
    "name": "GetNumBlueFlies",
    "signature": "int GetNumBlueFlies ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m144",
    "name": "GetNumBlueSpiders",
    "signature": "int GetNumBlueSpiders ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m145",
    "name": "GetNumBombs",
    "signature": "int GetNumBombs ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m146",
    "name": "GetNumCoins",
    "signature": "int GetNumCoins ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m147",
    "name": "GetNumGigaBombs",
    "signature": "int GetNumGigaBombs ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m148",
    "name": "GetNumKeys",
    "signature": "int GetNumKeys ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m149",
    "name": "GetOtherTwin",
    "signature": "[EntityPlayer](EntityPlayer.md) GetOtherTwin ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m150",
    "name": "GetPill",
    "signature": "[PillColor](enums/PillColor.md) GetPill ( int SlotId ) {: .copyable aria-label='Functions' data-altreturn='0' }",
    "description": ""
  },
  {
    "method_id": "m151",
    "name": "GetPillRNG",
    "signature": "[RNG](RNG.md) GetPillRNG ( [PillEffect](enums/PillEffect.md) ID ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m152",
    "name": "GetPlayerType",
    "signature": "[PlayerType](enums/PlayerType.md) GetPlayerType ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m153",
    "name": "GetPocketItem",
    "signature": "const PlayerPocketItem GetPocketItem ( int SlotId ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m154",
    "name": "GetPoopMana",
    "signature": "int GetPoopMana ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m155",
    "name": "GetPoopSpell",
    "signature": "[PoopSpellType](enums/PoopSpellType.md) GetPoopSpell ( int Position ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m156",
    "name": "GetRecentMovementVector",
    "signature": "const [Vector](Vector.md) GetRecentMovementVector ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m157",
    "name": "GetRottenHearts",
    "signature": "int GetRottenHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m158",
    "name": "GetShootingInput",
    "signature": "[Vector](Vector.md) GetShootingInput ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m159",
    "name": "GetShootingJoystick",
    "signature": "[Vector](Vector.md) GetShootingJoystick ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m160",
    "name": "GetSmoothBodyRotation",
    "signature": "float GetSmoothBodyRotation ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m161",
    "name": "GetSoulCharge",
    "signature": "int GetSoulCharge ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m162",
    "name": "GetSoulHearts",
    "signature": "int GetSoulHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m163",
    "name": "GetSubPlayer",
    "signature": "[EntityPlayer](EntityPlayer.md) GetSubPlayer ( ) {: .copyable aria-label='Functions' data-altreturn='nil' }",
    "description": ""
  },
  {
    "method_id": "m164",
    "name": "GetTearHitParams",
    "signature": "[TearParams](TearParams.md) GetTearHitParams ( [WeaponType](enums/WeaponType.md) WeaponType, float DamageScale = 1, int TearDisplacement = 1, Entity Source = nil ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m165",
    "name": "GetTearMovementInheritance",
    "signature": "[Vector](Vector.md) GetTearMovementInheritance ( [Vector](Vector.md) ShotDirection ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m166",
    "name": "GetTearPoisonDamage",
    "signature": "float GetTearPoisonDamage ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m167",
    "name": "GetTearRangeModifier",
    "signature": "int GetTearRangeModifier ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m168",
    "name": "GetTotalDamageTaken",
    "signature": "int GetTotalDamageTaken ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m169",
    "name": "GetTractorBeam",
    "signature": "[Entity](Entity.md) GetTractorBeam ( ) {: .copyable aria-label='Functions' data-altreturn='nil' }",
    "description": ""
  },
  {
    "method_id": "m170",
    "name": "GetTrinket",
    "signature": "[TrinketType](enums/TrinketType.md) GetTrinket ( int TrinketIndex ) {: .copyable aria-label='Functions' data-altreturn='0' }",
    "description": ""
  },
  {
    "method_id": "m171",
    "name": "GetTrinketMultiplier",
    "signature": "int GetTrinketMultiplier ( [TrinketType](enums/TrinketType.md) TrinketID ) {: .copyable aria-label='Functions' }",
    "description": "Gets the multiplier of a given Trinket effect. This is analog to the number of times the trinket effect is applied."
  },
  {
    "method_id": "m172",
    "name": "GetTrinketRNG",
    "signature": "[RNG](RNG.md) GetTrinketRNG ( [TrinketType](enums/TrinketType.md) TrinketID ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m173",
    "name": "GetVelocityBeforeUpdate",
    "signature": "const [Vector](Vector.md) GetVelocityBeforeUpdate ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m174",
    "name": "GetZodiacEffect",
    "signature": "[CollectibleType](enums/CollectibleType.md) GetZodiacEffect ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m175",
    "name": "HasCollectible",
    "signature": "boolean HasCollectible ( [CollectibleType](enums/CollectibleType.md) Type, boolean IgnoreModifiers = false ) {: .copyable aria-label='Functions' }",
    "description": "**IgnoreModifiers**: If set to true, only counts collectibles the player actually owns and ignores effects granted by items like Zodiac, 3 Dollar Bill and Lemegeton"
  },
  {
    "method_id": "m176",
    "name": "HasCurseMistEffect",
    "signature": "boolean HasCurseMistEffect ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m177",
    "name": "HasFullHearts",
    "signature": "boolean HasFullHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m178",
    "name": "HasFullHeartsAndSoulHearts",
    "signature": "boolean HasFullHeartsAndSoulHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m179",
    "name": "HasGoldenBomb",
    "signature": "boolean HasGoldenBomb ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m180",
    "name": "HasGoldenKey",
    "signature": "boolean HasGoldenKey ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m181",
    "name": "HasInvincibility",
    "signature": "boolean HasInvincibility ( [DamageFlag](enums/DamageFlag.md) Flags = 0 ) {: .copyable aria-label='Functions' }",
    "description": "returns true when player is in an invincibility state"
  },
  {
    "method_id": "m182",
    "name": "HasPlayerForm",
    "signature": "boolean HasPlayerForm ( [PlayerForm](enums/PlayerForm.md) Form ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m183",
    "name": "HasTimedItem",
    "signature": "boolean HasTimedItem ( ) {: .copyable aria-label='Functions' }",
    "description": "Returns true if you have a timed active item *(such as Brown Nugget)* in the first active slot"
  },
  {
    "method_id": "m184",
    "name": "HasTrinket",
    "signature": "boolean HasTrinket ( [TrinketType](enums/TrinketType.md) Type, boolean IgnoreModifiers = false ) {: .copyable aria-label='Functions' }",
    "description": "**IgnoreModifiers**: If set to true, only counts trinkets the player actually holds and ignores effects granted by other items"
  },
  {
    "method_id": "m185",
    "name": "HasWeaponType",
    "signature": "boolean HasWeaponType ( [WeaponType](enums/WeaponType.md) WeaponType ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m186",
    "name": "InitBabySkin",
    "signature": "void InitBabySkin ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m187",
    "name": "IsBlackHeart",
    "signature": "boolean IsBlackHeart ( int Heart ) {: .copyable aria-label='Functions' }",
    "description": "This can be used instead of GetBlackHearts to figure out which soul hearts are black hearts."
  },
  {
    "method_id": "m188",
    "name": "IsBoneHeart",
    "signature": "boolean IsBoneHeart ( int heart ) {: .copyable aria-label='Functions' }",
    "description": "This can be used to figure out the ordering of bone hearts amongst soul/black hearts."
  },
  {
    "method_id": "m189",
    "name": "IsCoopGhost",
    "signature": "boolean IsCoopGhost ( ) {: .copyable aria-label='Functions' }",
    "description": "In a multiplayer game, if a player dies, they will return as a tiny ghost. This method returns true if the player is a co-op ghost."
  },
  {
    "method_id": "m190",
    "name": "IsExtraAnimationFinished",
    "signature": "boolean IsExtraAnimationFinished ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m191",
    "name": "IsFullSpriteRendering",
    "signature": "boolean IsFullSpriteRendering ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m192",
    "name": "IsHeldItemVisible",
    "signature": "boolean IsHeldItemVisible ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m193",
    "name": "IsHoldingItem",
    "signature": "boolean IsHoldingItem ( ) {: .copyable aria-label='Functions' }",
    "description": "Is Player holding up an item (card/collectible/etc)"
  },
  {
    "method_id": "m194",
    "name": "IsItemQueueEmpty",
    "signature": "boolean IsItemQueueEmpty ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m195",
    "name": "IsP2Appearing",
    "signature": "boolean IsP2Appearing ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m196",
    "name": "IsPosInSpotLight",
    "signature": "boolean IsPosInSpotLight ( [Vector](Vector.md) Position ) {: .copyable aria-label='Functions' }",
    "description": "Returns true if the `position` is in the AOE of the **Night Light** item."
  },
  {
    "method_id": "m197",
    "name": "IsSubPlayer",
    "signature": "boolean IsSubPlayer ( ) {: .copyable aria-label='Functions' }",
    "description": "Returns true if the player object was returned from the `EntityPlayer.GetSubPlayer` method. (This method is not related to multiplayer.)"
  },
  {
    "method_id": "m198",
    "name": "NeedsCharge",
    "signature": "boolean NeedsCharge ( [ActiveSlot](enums/ActiveSlot.md) ActiveSlot = ActiveSlot.SLOT_PRIMARY ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m199",
    "name": "PlayExtraAnimation",
    "signature": "void PlayExtraAnimation ( string Animation ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m200",
    "name": "QueueExtraAnimation",
    "signature": "void QueueExtraAnimation ( string Animation ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m201",
    "name": "QueueItem",
    "signature": "void QueueItem ( [ItemConfigItem](ItemConfig_Item.md) Item, int Charge = 0, boolean Touched = false, boolean Golden = false, int VarData = 0 ) {: .copyable aria-label='Functions' }",
    "description": "When the player touches a collectible or trinket, they are not granted it immediately. Instead, the item is queued for the duration of the animation where the player holds the item above their head. When the animation is finished, the item in the queue will be granted. This method adds a new item to the item queue. If the player is not currently playing an animation, then the queued item will simply be awarded instantly."
  },
  {
    "method_id": "m202",
    "name": "RemoveBlackHeart",
    "signature": "void RemoveBlackHeart ( int BlackHeart ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m203",
    "name": "RemoveBlueFly",
    "signature": "void RemoveBlueFly ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m204",
    "name": "RemoveBlueSpider",
    "signature": "void RemoveBlueSpider ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m205",
    "name": "RemoveCollectible",
    "signature": "void RemoveCollectible ( [CollectibleType](enums/CollectibleType.md) Type, boolean IgnoreModifiers = false, [ActiveSlot](enums/ActiveSlot.md) ActiveSlot = ActiveSlot.SLOT_PRIMARY, boolean RemoveFromPlayerForm = true ) {: .copyable aria-label='Functions' }",
    "description": "**IgnoreModifiers**: Ignores collectible effects granted by other items (i.e. Void)"
  },
  {
    "method_id": "m206",
    "name": "RemoveCostume",
    "signature": "void RemoveCostume ( [ItemConfigItem](ItemConfig_Item.md) Item ) {: .copyable aria-label='Functions' }",
    "description": "Removes a given costume based on its item config entry."
  },
  {
    "method_id": "m207",
    "name": "RemoveCurseMistEffect",
    "signature": "void RemoveCurseMistEffect ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m208",
    "name": "RemoveGoldenBomb",
    "signature": "void RemoveGoldenBomb ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m209",
    "name": "RemoveGoldenKey",
    "signature": "void RemoveGoldenKey ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m210",
    "name": "RemoveSkinCostume",
    "signature": "void RemoveSkinCostume ( ) {: .copyable aria-label='Functions' }",
    "description": "Removes player-specific costumes like Magdalene's hair or Cain's eyepatch."
  },
  {
    "method_id": "m211",
    "name": "RenderBody",
    "signature": "void RenderBody ( [Vector](Vector.md) position ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m212",
    "name": "RenderGlow",
    "signature": "void RenderGlow ( [Vector](Vector.md) position ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m213",
    "name": "RenderHead",
    "signature": "void RenderHead ( [Vector](Vector.md) position ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m214",
    "name": "RenderTop",
    "signature": "void RenderTop ( [Vector](Vector.md) position ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m215",
    "name": "ReplaceCostumeSprite",
    "signature": "void ReplaceCostumeSprite ( [ItemConfigItem](ItemConfig_Item.md) Item, string SpritePath, int SpriteId ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m216",
    "name": "ResetDamageCooldown",
    "signature": "void ResetDamageCooldown ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m217",
    "name": "ResetItemState",
    "signature": "void ResetItemState ( ) {: .copyable aria-label='Functions' }",
    "description": "[Room](Room.md) transitions call this to prevent lock ups."
  },
  {
    "method_id": "m218",
    "name": "RespawnFamiliars",
    "signature": "void RespawnFamiliars ( ) {: .copyable aria-label='Functions' }",
    "description": "Respawns all familiars associated to the player."
  },
  {
    "method_id": "m219",
    "name": "Revive",
    "signature": "void Revive ( ) {: .copyable aria-label='Functions' }",
    "description": "Revives the player."
  },
  {
    "method_id": "m220",
    "name": "SetActiveCharge",
    "signature": "void SetActiveCharge ( int Charge, [ActiveSlot](enums/ActiveSlot.md) ActiveSlot = ActiveSlot.SLOT_PRIMARY ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m221",
    "name": "SetBloodCharge",
    "signature": "void SetBloodCharge ( int Amount ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m222",
    "name": "SetCard",
    "signature": "void SetCard ( int SlotId, [Card](enums/Card.md) ID ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m223",
    "name": "SetFullHearts",
    "signature": "void SetFullHearts ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m224",
    "name": "SetMinDamageCooldown",
    "signature": "void SetMinDamageCooldown ( int DamageCooldown ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m225",
    "name": "SetPill",
    "signature": "void SetPill ( int SlotId, [PillColor](enums/PillColor.md) Pill ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m226",
    "name": "SetPocketActiveItem",
    "signature": "void SetPocketActiveItem ( [CollectibleType](enums/CollectibleType.md) Type, [ActiveSlot](enums/ActiveSlot.md) Slot, boolean KeepInPools ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m227",
    "name": "SetShootingCooldown",
    "signature": "void SetShootingCooldown ( int Cooldown ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m228",
    "name": "SetSoulCharge",
    "signature": "void SetSoulCharge ( int Amount ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m229",
    "name": "SetTargetTrapDoor",
    "signature": "void SetTargetTrapDoor ( [GridEntity](GridEntity.md) TrapDoor ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m230",
    "name": "ShootRedCandle",
    "signature": "void ShootRedCandle ( [Vector](Vector.md) Direction ) {: .copyable aria-label='Functions' }",
    "description": "for ghost pepper item + poop and farts"
  },
  {
    "method_id": "m231",
    "name": "SpawnMawOfVoid",
    "signature": "[EntityLaser](EntityLaser.md) SpawnMawOfVoid ( int Timeout ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m232",
    "name": "StopExtraAnimation",
    "signature": "void StopExtraAnimation ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m233",
    "name": "SwapActiveItems",
    "signature": "void SwapActiveItems ( ) {: .copyable aria-label='Functions' }",
    "description": "Swaps active items in the **Schoolbag** activeslot"
  },
  {
    "method_id": "m234",
    "name": "ThrowBlueSpider",
    "signature": "[Entity](Entity.md) ThrowBlueSpider ( [Vector](Vector.md) Position, [Vector](Vector.md) Target ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m235",
    "name": "ThrowFriendlyDip",
    "signature": "[EntityFamiliar](EntityFamiliar.md) ThrowFriendlyDip ( int Subtype, [Vector](Vector.md) Position, [Vector](Vector.md) Target ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m236",
    "name": "ThrowHeldEntity",
    "signature": "[Entity](Entity.md) ThrowHeldEntity ( [Vector](Vector.md) Velocity ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m237",
    "name": "TriggerBookOfVirtues",
    "signature": "void TriggerBookOfVirtues ( [CollectibleType](enums/CollectibleType.md) Type = CollectibleType.COLLECTIBLE_NULL, int Charge = 0 ) {: .copyable aria-label='Functions' }",
    "description": "Works only if the player has the **Book of Virtues** item, otherwise does nothing"
  },
  {
    "method_id": "m238",
    "name": "TryHoldEntity",
    "signature": "boolean TryHoldEntity ( [Entity](Entity.md) Entity ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m239",
    "name": "TryHoldTrinket",
    "signature": "boolean TryHoldTrinket ( [TrinketType](enums/TrinketType.md) Type ) {: .copyable aria-label='Functions' }",
    "description": "Returns true if an active item pickup cooldown is over. returns true if trinket can be added, else false"
  },
  {
    "method_id": "m240",
    "name": "TryRemoveCollectibleCostume",
    "signature": "void TryRemoveCollectibleCostume ( [CollectibleType](enums/CollectibleType.md) Collectible, boolean KeepPersistent ) {: .copyable aria-label='Functions' }",
    "description": "Tries to remove a costume of the given collectible. `KeepPersistent` is used to define if persistent costumes should be removed. If its set to `false`, it will only remove temporary costumes."
  },
  {
    "method_id": "m241",
    "name": "TryRemoveNullCostume",
    "signature": "void TryRemoveNullCostume ( [NullItemID](enums/NullItemID.md) NullId ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m242",
    "name": "TryRemoveTrinket",
    "signature": "boolean TryRemoveTrinket ( [TrinketType](enums/TrinketType.md) Type ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m243",
    "name": "TryRemoveTrinketCostume",
    "signature": "void TryRemoveTrinketCostume ( [TrinketType](enums/TrinketType.md) Trinket ) {: .copyable aria-label='Functions' }",
    "description": "Tries to remove a trinket costume"
  },
  {
    "method_id": "m244",
    "name": "TryUseKey",
    "signature": "boolean TryUseKey ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m245",
    "name": "UpdateCanShoot",
    "signature": "void UpdateCanShoot ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m246",
    "name": "UseActiveItem",
    "signature": "void UseActiveItem ( [CollectibleType](enums/CollectibleType.md) Item, [UseFlags](enums/UseFlag.md) UseFlags = 0, [ActiveSlot](enums/ActiveSlot.md) Slot = -1, int CustomVarData = 0 ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m247",
    "name": "void UseActiveItem ( [CollectibleType](enums/CollectibleType.md) Item, boolean ShowAnim = false, boolean KeepActiveItem = false, boolean AllowNonMainPlayer = true, boolean ToAddCostume = false, [ActiveSlot](enums/ActiveSlot.md) Slot = -1, int CustomVarData = 0 )",
    "signature": "void UseCard ( [Card](enums/Card.md) ID, [UseFlags](enums/UseFlag.md) UseFlags = 0 ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m248",
    "name": "UsePill",
    "signature": "void UsePill ( [PillEffect](enums/PillEffect.md) ID, [PillColor](enums/PillColor.md) PillColor, [UseFlags](enums/UseFlag.md) UseFlags = 0  ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m249",
    "name": "UsePoopSpell",
    "signature": "void UsePoopSpell ( [PoopSpellType](enums/PoopSpellType.md) type ) {: .copyable aria-label='Functions' }",
    "description": "Triggers one of Tainted ???'s poop spells (see [PoopSpellType](enums/PoopSpellType.md) enum)"
  },
  {
    "method_id": "m250",
    "name": "WillPlayerRevive",
    "signature": "boolean WillPlayerRevive ( ) {: .copyable aria-label='Functions' }",
    "description": "This function will return true if the player has one or more extra lives or if a conditional revival item will work on the next death."
  },
  {
    "method_id": "m251",
    "name": "BabySkin",
    "signature": "[BabySubType](enums/BabySubType.md) BabySkin  {: .copyable aria-label='Variables' }",
    "description": "P2 Skin section Used to hold the selected skin (in case of glitched baby it will pick a random one)"
  },
  {
    "method_id": "m252",
    "name": "CanFly",
    "signature": "boolean CanFly  {: .copyable aria-label='Variables' }",
    "description": "Player stat - Only change this in a callback to MC_EVALUATE_CACHE. Can the player fly over rocks and pits?"
  },
  {
    "method_id": "m253",
    "name": "ControllerIndex",
    "signature": "const int ControllerIndex  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m254",
    "name": "ControlsCooldown",
    "signature": "int ControlsCooldown  {: .copyable aria-label='Variables' }",
    "description": "Specifies the number of frames the player's controls should be disabled. Decrements by 1 every frame, until it reaches 0. Used by the paralysis pill effect."
  },
  {
    "method_id": "m255",
    "name": "ControlsEnabled",
    "signature": "boolean ControlsEnabled  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m256",
    "name": "Damage",
    "signature": "float Damage  {: .copyable aria-label='Variables' }",
    "description": "Player stat - Only change this in a callback to MC_EVALUATE_CACHE.  **This is equal to the Damage Stat.**  How much damage do the players tears or other main weapons do?"
  },
  {
    "method_id": "m257",
    "name": "FireDelay",
    "signature": "float FireDelay  {: .copyable aria-label='Variables' }",
    "description": "How long until the player can spawn their next tear?"
  },
  {
    "method_id": "m258",
    "name": "FriendBallEnemy",
    "signature": "const EntityDesc FriendBallEnemy  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m259",
    "name": "HeadFrameDelay",
    "signature": "int HeadFrameDelay  {: .copyable aria-label='Variables' }",
    "description": "Specifies the number of frames the player's head should be playing the shooting animation. Decrements by 1 every frame, until it reaches -1."
  },
  {
    "method_id": "m260",
    "name": "IBSCharge",
    "signature": "float IBSCharge  {: .copyable aria-label='Variables' }",
    "description": "Internally used by IBS, increases based on damage dealt, range is 0-1"
  },
  {
    "method_id": "m261",
    "name": "ItemHoldCooldown",
    "signature": "int ItemHoldCooldown  {: .copyable aria-label='Variables' }",
    "description": "Used for avoiding player get stucked between rocks when switching a flying item with other active item."
  },
  {
    "method_id": "m262",
    "name": "LaserColor",
    "signature": "[Color](Color.md) LaserColor  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m263",
    "name": "Luck",
    "signature": "float Luck  {: .copyable aria-label='Variables' }",
    "description": "Player stat - Only change this in a callback to MC_EVALUATE_CACHE.  **This is equal to the Luck Stat.**  Better luck generally means better random events."
  },
  {
    "method_id": "m264",
    "name": "MaxFireDelay",
    "signature": "float MaxFireDelay  {: .copyable aria-label='Variables' }",
    "description": "Player stat - Only change this in a callback to MC_EVALUATE_CACHE.  **This is equal to the Tears Stat.**  How long between each tear can spawn?"
  },
  {
    "method_id": "m265",
    "name": "MoveSpeed",
    "signature": "float MoveSpeed  {: .copyable aria-label='Variables' }",
    "description": "Player stat - Only change this in a callback to MC_EVALUATE_CACHE.  **This is equal to the Speed Stat.**  How fast can the player move?"
  },
  {
    "method_id": "m266",
    "name": "QueuedItem",
    "signature": "[QueueItemData](QueueItemData.md) QueuedItem  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m267",
    "name": "SamsonBerserkCharge",
    "signature": "int SamsonBerserkCharge  {: .copyable aria-label='Variables' }",
    "description": "Internally used by Tainted Samson, increases based on damage dealt, range is 0-100000"
  },
  {
    "method_id": "m268",
    "name": "SecondaryActiveItem",
    "signature": "[ActiveItemDesc](PlayerTypes_ActiveItemDesc.md) SecondaryActiveItem  {: .copyable aria-label='Variables' data-altreturn='nil' }",
    "description": ""
  },
  {
    "method_id": "m269",
    "name": "ShotSpeed",
    "signature": "float ShotSpeed  {: .copyable aria-label='Variables' }",
    "description": "Player stat - Only change this in a callback to MC_EVALUATE_CACHE.  **This is equal to the ShotSpeed Stat.**"
  },
  {
    "method_id": "m270",
    "name": "TearColor",
    "signature": "[Color](Color.md) TearColor  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m271",
    "name": "TearFallingAcceleration",
    "signature": "float TearFallingAcceleration  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m272",
    "name": "TearFallingSpeed",
    "signature": "float TearFallingSpeed  {: .copyable aria-label='Variables' }",
    "description": "Player stat - Only change this in a callback to MC_EVALUATE_CACHE. How fast is the tear moving up or down when it spawns? Affects range."
  },
  {
    "method_id": "m273",
    "name": "TearFlags",
    "signature": "[TearFlags](enums/TearFlags.md) TearFlags {: .copyable aria-label='Variables' }",
    "description": "Player stat - Only change this in a callback to MC_EVALUATE_CACHE. Various [TearFlags](enums/TearFlags.md)."
  },
  {
    "method_id": "m274",
    "name": "TearHeight",
    "signature": "float TearHeight  {: .copyable aria-label='Variables' }",
    "description": "Player stat - Only change this in a callback to MC_EVALUATE_CACHE. How high above the ground is the tear when it spawns?"
  },
  {
    "method_id": "m275",
    "name": "TearRange",
    "signature": "float TearRange  {: .copyable aria-label='Variables' }",
    "description": "Player stat - Only change this in a callback to MC_EVALUATE_CACHE. How far should a tear go when it spawns?"
  },
  {
    "method_id": "m276",
    "name": "TearsOffset",
    "signature": "[Vector](Vector.md) TearsOffset  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "EntityPlayer 类代表玩家实体，提供大量方法用于操作玩家状态，包括生命值、消耗品、道具、攻击、动画、属性等，是 Mod 开发中最核心的玩家交互接口。",
    "use_cases": [
      "修改玩家生命、炸弹、钥匙等消耗品数量",
      "添加或移除道具、卡牌、药丸和饰品",
      "发射眼泪、炸弹等攻击",
      "查询玩家属性（伤害、射速、幸运等）",
      "控制玩家动画和装扮"
    ],
    "key_methods": [
      "AddCollectible",
      "RemoveCollectible",
      "AddHearts",
      "FireTear",
      "GetPlayerType"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "添加或移除黑心（每单位半颗心）。",
      "use_cases": ["增加黑心数量", "扣除黑心"],
      "key_methods": ["AddBlackHearts", "AddSoulHearts", "AddHearts"]
    },
    {
      "method_id": "m002",
      "summary": "添加血量充能，仅对堕化伯大妮有效。",
      "use_cases": ["增加伯大妮的血量充能"],
      "key_methods": ["AddBloodCharge", "AddSoulCharge", "GetBloodCharge"]
    },
    {
      "method_id": "m003",
      "summary": "生成蓝苍蝇攻击敌人，数量受饰品鱼尾影响。",
      "use_cases": ["制造额外攻击随从"],
      "key_methods": ["AddBlueFlies", "AddBlueSpider", "AddFriendlyDip"]
    },
    {
      "method_id": "m004",
      "summary": "在指定位置生成一只蓝蜘蛛。",
      "use_cases": ["创建爪机攻击单位"],
      "key_methods": ["AddBlueSpider", "AddBlueFlies", "ThrowBlueSpider"]
    },
    {
      "method_id": "m005",
      "summary": "添加或移除炸弹数量。",
      "use_cases": ["增加炸弹上限", "减少炸弹数"],
      "key_methods": ["AddBombs", "GetNumBombs", "AddKeys"]
    },
    {
      "method_id": "m006",
      "summary": "添加或移除骨心（每个单位一颗骨心）。",
      "use_cases": ["增加骨心容器"],
      "key_methods": ["AddBoneHearts", "AddGoldenHearts", "AddSoulHearts"]
    },
    {
      "method_id": "m007",
      "summary": "添加或移除碎心。",
      "use_cases": ["增加碎心数量"],
      "key_methods": ["AddBrokenHearts", "GetBrokenHearts", "AddHearts"]
    },
    {
      "method_id": "m008",
      "summary": "标记指定的缓存标签，下次缓存重算时将更新相应属性。",
      "use_cases": ["刷新伤害、射速等统计"],
      "key_methods": ["AddCacheFlags", "EvaluateItems", "GetEffects"]
    },
    {
      "method_id": "m009",
      "summary": "给予一张卡牌。",
      "use_cases": ["直接获得指定卡牌"],
      "key_methods": ["AddCard", "GetCard", "SetCard"]
    },
    {
      "method_id": "m010",
      "summary": "添加或移除金币。",
      "use_cases": ["增加金币", "减少金币"],
      "key_methods": ["AddCoins", "GetNumCoins", "AddBombs"]
    },
    {
      "method_id": "m011",
      "summary": "添加道具，支持设置充能、首次拾取、主动槽位和VarData。",
      "use_cases": ["给予玩家道具", "模拟首次拾取"],
      "key_methods": ["AddCollectible", "RemoveCollectible", "HasCollectible"]
    },
    {
      "method_id": "m012",
      "summary": "添加道具（重载），额外指定道具池类型。",
      "use_cases": ["指定道具池的道具获取"],
      "key_methods": ["AddCollectible", "CanAddCollectible", "GetCollectibleRNG"]
    },
    {
      "method_id": "m013",
      "summary": "添加基于ItemConfigItem的装扮。",
      "use_cases": ["动态更换角色外观"],
      "key_methods": ["AddCostume", "RemoveCostume", "ClearCostumes"]
    },
    {
      "method_id": "m014",
      "summary": "添加诅咒迷雾效果。",
      "use_cases": ["触发迷雾视觉效果"],
      "key_methods": ["AddCurseMistEffect", "RemoveCurseMistEffect", "HasCurseMistEffect"]
    },
    {
      "method_id": "m015",
      "summary": "增加精准射手充能层数。",
      "use_cases": ["提升精准射手伤害加成"],
      "key_methods": ["AddDeadEyeCharge", "ClearDeadEyeCharge", "FireTear"]
    },
    {
      "method_id": "m016",
      "summary": "添加3美元钞票的随机效果。",
      "use_cases": ["随机获得短暂道具效果"],
      "key_methods": ["AddDollarBillEffect", "GetEffects", "AddCacheFlags"]
    },
    {
      "method_id": "m017",
      "summary": "添加或移除永恒之心（每单位半颗心）。",
      "use_cases": ["增加永恒之心"],
      "key_methods": ["AddEternalHearts", "GetEternalHearts", "AddHearts"]
    },
    {
      "method_id": "m018",
      "summary": "生成一个友好的小屎角色。",
      "use_cases": ["召唤Dip随从"],
      "key_methods": ["AddFriendlyDip", "ThrowFriendlyDip", "AddBlueFlies"]
    },
    {
      "method_id": "m019",
      "summary": "添加巨型炸弹数量，需提前增加普通炸弹。",
      "use_cases": ["增加巨型炸弹"],
      "key_methods": ["AddGigaBombs", "GetNumGigaBombs", "AddBombs"]
    },
    {
      "method_id": "m020",
      "summary": "添加一个金炸弹效果。",
      "use_cases": ["获得无限炸弹效果"],
      "key_methods": ["AddGoldenBomb", "RemoveGoldenBomb", "HasGoldenBomb"]
    },
    {
      "method_id": "m021",
      "summary": "添加或移除金心（每个单位一颗金心）。",
      "use_cases": ["增加金心容器"],
      "key_methods": ["AddGoldenHearts", "GetGoldenHearts", "AddBoneHearts"]
    },
    {
      "method_id": "m022",
      "summary": "添加一个金钥匙效果。",
      "use_cases": ["获得无限钥匙效果"],
      "key_methods": ["AddGoldenKey", "RemoveGoldenKey", "HasGoldenKey"]
    },
    {
      "method_id": "m023",
      "summary": "添加或移除红心（每单位半颗心），填充心容器。",
      "use_cases": ["恢复红心", "扣除生命值"],
      "key_methods": ["AddHearts", "GetHearts", "AddMaxHearts"]
    },
    {
      "method_id": "m024",
      "summary": "添加魂火（来自美德之书），可指定道具类型。",
      "use_cases": ["召唤特殊魂火环绕物"],
      "key_methods": ["AddItemWisp", "AddWisp", "TriggerBookOfVirtues"]
    },
    {
      "method_id": "m025",
      "summary": "添加苍蝇罐子中的苍蝇数量。",
      "use_cases": ["增加苍蝇罐子存量"],
      "key_methods": ["AddJarFlies", "GetJarFlies", "AddJarHearts"]
    },
    {
      "method_id": "m026",
      "summary": "添加心罐子中的生命储存量。",
      "use_cases": ["增加心形罐子储存"],
      "key_methods": ["AddJarHearts", "GetJarHearts", "AddJarFlies"]
    },
    {
      "method_id": "
```
