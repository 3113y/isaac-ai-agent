# DeepSeek Context

- class: GlobalFunctions
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:24:27.820150

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

类名：GlobalFunctions

原始 md 文档（该类完整文档，可能已截断）：
# Global Functions
## Constructors
### BitSet128 () {: aria-label='Constructors' }
[ ](#){: .reporplus .tooltip .badge }
#### [BitSet128](BitSet128.md) BitSet128 ( int Low = 0, int High = 0 ) {: .copyable aria-label='Constructors' }

Constructor for the "BitSet128" class.

[BitSet128](BitSet128.md) is used as a storage system for flags and other bit-wise evaluated values that exceed the numeric limits of the default 64-bit integers which only allow for up to 64 flags to be defined. [BitSet128](BitSet128.md) allows for up to 128 Flags by spliting the bitset into a "lower" and "higher" part. Those parts are represented by a simple 64bit integer number.
___
### Color () {: aria-label='Constructors' }
[ ](#){: .reporplus .tooltip .badge }
#### [Color](Color.md) Color ( float R, float G, float B, float A = 1, float RO = 0, float GO = 0, float BO = 0 ) {: .copyable aria-label='Constructors' }

Constructor for the "[Color](Color.md)" class.

When using the [Font](Font.md) class, use [KColor()](KColor.md) instead.

Colors are made of three separate components, tint, colorize and offset. Tint acts like a color multiplicator. Offset is a color which is added after the tint is applied. Colorize is complicated. See the `:::lua SetColorize()` function for a detailed description.

R, G, B, A, RO, GO and BO accept numbers between 0 and 1.
___
### Entity·Ptr () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [EntityPtr](EntityPtr.md) EntityPtr ( [Entity](Entity.md) entity ) {: .copyable aria-label='Constructors' }

___
### Entity·Ref () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [EntityRef](EntityRef.md) EntityRef ( [Entity](Entity.md) entity ) {: .copyable aria-label='Constructors' }

___
### Font () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [Font](Font.md) Font ( ) {: .copyable aria-label='Constructors' }

Constructor for the "[Font](Font.md)" class.

???- example "Example Code"
    Example usage.
    ```lua
    local f = Font() -- init font object
    f:Load("font/terminus.fnt") -- load a font into the font object
    f:DrawString("Hello World!",60,50,KColor(1,1,1,1),0,true) -- render string with loaded font on position 60x50y

    ```

___
### Game () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [Game](Game.md) Game ( ) {: .copyable aria-label='Constructors' }

Returns a [Game](Game.md) object.

???- example "Example Code"
    Example usage:
    ```lua
    Game():IsPaused()
    --returns true if the game is paused

    ```
___
### KColor () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [KColor](KColor.md) KColor ( float red, float green, float blue, float alpha ) {: .copyable aria-label='Constructors' }

Constructor for the "[KColor](KColor.md)" class.

???+ note "Notes"
	"KColor" is only used in the [Font](Font.md) class. For most other situations you will need to use the [Color()](Color.md) constructor.

___
### Music·Manager () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [MusicManager](MusicManager.md) MusicManager ( ) {: .copyable aria-label='Constructors' }

Returns a [MusicManager](MusicManager.md) object.

???- example "Example Code"
    Example usage:
    ```lua
    MusicManager():Disable()

    ```
___
### Projectile·Params () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [ProjectileParams](ProjectileParams.md) ProjectileParams ( ) {: .copyable aria-label='Constructors' }

___
### Register·Mod () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [Mod Reference](ModReference.md) RegisterMod ( string modName, int apiVersion ) {: .copyable aria-label='Constructors' }

Method to define a mod in the game. This needs to be defined to handle callbacks and save data in your mod.

Returns a table which acts as the [Mod Reference](ModReference.md).

???- example "Example Code"
    ```lua
    local yourMod = RegisterMod("someMod", 1)

    ```

___
### RNG () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [RNG](RNG.md) RNG ( ) {: .copyable aria-label='Constructors' }

___
### SFXManager () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [SFXManager](SFXManager.md) SFXManager ( ) {: .copyable aria-label='Constructors' }

Returns a [SFXManager](SFXManager.md) object.

???- example "Example Code"
    Example usage:
    ```lua
    SFXManager():Stop(SoundEffect.SOUND_1UP)

    ```
___
### Sprite () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [Sprite](Sprite.md) Sprite ( ) {: .copyable aria-label='Constructors' }

___
### Vector () {: aria-label='Constructors' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) Vector ( float x, float y) {: .copyable aria-label='Constructors' }

___
## Functions
### Get·Ptr·Hash () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### int GetPtrHash ( Object object ) {: .copyable aria-label='Functions' }
Returns a hash-value of the pointer given as an input value. Valid inputs are any Isaac object, including `:::lua Entity`, `:::lua Room`, `:::lua RNG`, `:::lua Sprite`, `:::lua Game` etc.

It can be used to easily compare two entities, making equality checks very easy.

**Example:**

If you spawn a certain entity, save it in a variable and then compare it to the `:::lua entity` parameter in `:::lua MC_ENTITY_TAKE_DMG`, this comparison will never be true even if both variables refer to the exact same entity in the game. `:::lua GetPtrHash()` turns pointer into a fixed number, which makes comparisons easier.

???- example "Example Code"
    Example on check if two entities saved in different variables are the same.
    ```lua
    -- don't do it like this
    if entity1 == entity2 then
        -- this will always be false, because two different references on a pointer are not equal
    end
    -- use GetPtrHash() to compare them
    if GetPtrHash(entity1) == GetPtrHash(entity2) then
        -- this will be true, when the pointer of both variables point to the same object.
    end

    ```

___
### Random () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### int Random ( ) {: .copyable aria-label='Functions' }
Returns a random integer between 0 and 2^32. It is tested to be inclusive on the lower end and exclusive on the higher end.

Since this function can return 0, you cannot safely use it as the seed for an RNG object, since RNG objects with a seed of 0 crash the game. It is recommended to abstract away this failure case by using a helper function that arbitrarily sets the seed to 1 when the seed is 0.

___
### Random·Vector () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### [Vector](Vector.md) RandomVector ( ) {: .copyable aria-label='Functions' }
Returns a random vector with length 1. Multiply this vector by a number for larger random vectors.
___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "BitSet128",
    "signature": "[BitSet128](BitSet128.md) BitSet128 ( int Low = 0, int High = 0 ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "Color",
    "signature": "[Color](Color.md) Color ( float R, float G, float B, float A = 1, float RO = 0, float GO = 0, float BO = 0 ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "EntityPtr",
    "signature": "[EntityPtr](EntityPtr.md) EntityPtr ( [Entity](Entity.md) entity ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "EntityRef",
    "signature": "[EntityRef](EntityRef.md) EntityRef ( [Entity](Entity.md) entity ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "Font",
    "signature": "[Font](Font.md) Font ( ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "Game",
    "signature": "[Game](Game.md) Game ( ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "KColor",
    "signature": "[KColor](KColor.md) KColor ( float red, float green, float blue, float alpha ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "MusicManager",
    "signature": "[MusicManager](MusicManager.md) MusicManager ( ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "ProjectileParams",
    "signature": "[ProjectileParams](ProjectileParams.md) ProjectileParams ( ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "RegisterMod",
    "signature": "[Mod Reference](ModReference.md) RegisterMod ( string modName, int apiVersion ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "RNG",
    "signature": "[RNG](RNG.md) RNG ( ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "SFXManager",
    "signature": "[SFXManager](SFXManager.md) SFXManager ( ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "Sprite",
    "signature": "[Sprite](Sprite.md) Sprite ( ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m014",
    "name": "Vector",
    "signature": "[Vector](Vector.md) Vector ( float x, float y) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m015",
    "name": "GetPtrHash",
    "signature": "int GetPtrHash ( Object object ) {: .copyable aria-label='Functions' }",
    "description": "Returns a hash-value of the pointer given as an input value. Valid inputs are any Isaac object, including `:::lua Entity`, `:::lua Room`, `:::lua RNG`, `:::lua Sprite`, `:::lua Game` etc."
  },
  {
    "method_id": "m016",
    "name": "Random",
    "signature": "int Random ( ) {: .copyable aria-label='Functions' }",
    "description": "Returns a random integer between 0 and 2^32. It is tested to be inclusive on the lower end and exclusive on the higher end."
  },
  {
    "method_id": "m017",
    "name": "RandomVector",
    "signature": "[Vector](Vector.md) RandomVector ( ) {: .copyable aria-label='Functions' }",
    "description": "Returns a random vector with length 1. Multiply this vector by a number for larger random vectors."
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "《以撒的结合》全局函数集，提供各种核心对象的构造函数、管理器获取以及实用工具函数，是 mod 开发的基础接口。",
    "use_cases": [
      "Mod 注册与初始化",
      "创建游戏实体、颜色、字体等对象",
      "获取音乐、音效管理器",
      "生成随机数或随机向量",
      "比较不同引用是否指向同一实体"
    ],
    "key_methods": [
      "RegisterMod",
      "Game",
      "GetPtrHash",
      "Random",
      "SFXManager"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "构造一个 128 位标志集对象，用于存储超过 64 个布尔标志或位运算值。",
      "use_cases": [
        "存储大量解锁标志",
        "实现自定义状态位"
      ],
      "key_methods": [
        "BitSet128"
      ]
    },
    {
      "method_id": "m002",
      "summary": "构造一个通用颜色对象，用于渲染中的色调、偏移等设置。",
      "use_cases": [
        "设置实体颜色",
        "绘制彩色文本"
      ],
      "key_methods": [
        "Color",
        "KColor"
      ]
    },
    {
      "method_id": "m003",
      "summary": "创建一个不拥有所有权的实体指针对象，用于安全引用可能被销毁的实体。",
      "use_cases": [
        "在回调中保存实体引用",
        "延迟访问实体"
      ],
      "key_methods": [
        "EntityPtr",
        "EntityRef",
        "GetPtrHash"
      ]
    },
    {
      "method_id": "m004",
      "summary": "创建一个实体引用对象，提供对实体的访问并能在实体无效时返回 nil。",
      "use_cases": [
        "安全获取实体状态",
        "在实体可能消失时进行条件判断"
      ],
      "key_methods": [
        "EntityRef",
        "EntityPtr",
        "GetPtrHash"
      ]
    },
    {
      "method_id": "m005",
      "summary": "创建一个字体对象，用于加载位图字体并在屏幕上绘制字符串。",
      "use_cases": [
        "自定义 UI 文本",
        "绘制 HUD 信息"
      ],
      "key_methods": [
        "Font",
        "KColor"
      ]
    },
    {
      "method_id": "m006",
      "summary": "获取当前游戏实例对象，用于查询暂停状态、房间信息等全局游戏属性。",
      "use_cases": [
        "检测游戏是否暂停",
        "访问游戏整体设置"
      ],
      "key_methods": [
        "Game"
      ]
    },
    {
      "method_id": "m007",
      "summary": "构造专门用于 Font 对象的颜色，提供 RGB 及透明度。",
      "use_cases": [
        "设置字体颜色",
        "与 Font:DrawString 配合"
      ],
      "key_methods": [
        "KColor",
        "Font",
        "Color"
      ]
    },
    {
      "method_id": "m008",
      "summary": "获取音乐管理器对象，用于控制背景音乐的播放、暂停等。",
      "use_cases": [
        "禁用背景音乐",
        "切换音乐曲目"
      ],
      "key_methods": [
        "MusicManager",
        "SFXManager"
      ]
    },
    {
      "method_id": "m009",
      "summary": "创建一个抛射体参数对象，用于定义发射子弹时的各种属性。",
      "use_cases": [
        "自定义弹幕行为",
        "设置子弹速度、伤害等"
      ],
      "key_methods": [
        "ProjectileParams"
      ]
    },
    {
      "method_id": "m010",
      "summary": "注册当前 mod，返回 mod 引用，是所有 mod 必须首先调用的入口函数。",
      "use_cases": [
        "mod 初始化",
        "注册回调与保存数据"
      ],
      "key_methods": [
        "RegisterMod"
      ]
    },
    {
      "method_id": "m011",
      "summary": "创建一个新的随机数生成器对象，用于可控的随机序列。",
      "use_cases": [
        "控制物品生成随机",
        "实现可复现的随机"
      ],
      "key_methods": [
        "RNG",
        "Random"
      ]
    },
    {
      "method_id": "m012",
      "summary": "获取音效管理器对象，用于播放、停止游戏音效。",
      "use_cases": [
        "播放自定义音效",
        "停止特定音效"
      ],
      "key_methods": [
        "SFXManager",
        "MusicManager"
      ]
    },
    {
      "method_id": "m013",
      "summary": "创建一个精灵对象，用于加载和显示动画帧。",
      "use_cases": [
        "渲染自定义实体",
        "界面动画"
      ],
      "key_methods": [
        "Sprite"
      ]
    },
    {
      "method_id": "m014",
      "summary": "创建一个二维向量对象，用于位置、速度等数学运算。",
      "use_cases": [
        "设置实体位置",
        "计算移动方向"
      ],
      "key_methods": [
        "Vector",
        "RandomVector"
      ]
    },
    {
      "method_id": "m015",
      "summary": "返回对象指针的哈希值，用于可靠判断两个引用是否指向同一游戏对象。",
      "use_cases": [
        "比较回调中的 entity 与保存的 entity",
        "避免直接指针比较的错误"
      ],
      "key_methods": [
        "GetPtrHash",
        "EntityPtr",
        "EntityRef"
      ]
    },
    {
      "method_id": "m016",
      "summary": "返回一个 0 到 2^32 之间的伪随机整数，适合非种子的简单随机需求。",
      "use_cases": [
        "生成随机偏移",
        "临时决定概率"
      ],
      "key_methods": [
        "Random",
        "RNG"
      ]
    },
    {
      "method_id": "m017",
      "summary": "返回一个长度为 1 的随机方向向量，可乘以长度以获得任意距离的随机方向。",
      "use_cases": [
        "生成随机弹幕方向",
        "物品随机掉落偏移"
      ],
      "key_methods": [
        "RandomVector",
        "Vector"
      ]
    }
  ]
}
```
