# DeepSeek Context

- class: Mod Reference
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:53:59.862784

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

类名：Mod Reference

原始 md 文档（该类完整文档，可能已截断）：
# Class "Mod Reference"

???+ info
    You can get this class by using the following functions:

    * [RegisterMod()](GlobalFunctions.md#registermod)

## Functions
### Add·Callback () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddCallback ( [ModCallbacks](enums/ModCallbacks.md) callbackId, function callbackFn, int entityId ) {: .copyable aria-label='Functions' }
___
### Add·Priority·Callback () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void AddPriorityCallback ( [ModCallbacks](enums/ModCallbacks.md) callbackId, [CallbackPriority](enums/CallbackPriority.md) priority, function callbackFn, int entityId ) {: .copyable aria-label='Functions' }

Allows modders to specify that a callback function should run earlier or later than normal relative to other functions added to that callback.
___
### Has·Data () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean HasData ( ) {: .copyable aria-label='Functions' }

Returns "true" if your mod has Data stored using the "SaveData()" function. Aka. if there is a "saveX.dat" file in your mod folder. There are 3 "saveX.dat" files, one per Savegame. They are stored in the mod's folder next to the "main.lua" file. The number indicates the savegame it corresponds to. The number will be determined automatically by the game.
___
### Load·Data () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### string LoadData ( ) {: .copyable aria-label='Functions' }

Returns a string that was stored in a "saveX.dat" file using the "SaveData()" function. If there is no "saveX.dat" file in your mod, this function will return an empty string.
There are 3 "saveX.dat" files, one per Savegame. They are stored in the mod's folder next to the "main.lua" file. The number indicates the savegame it corresponds to. The number will be determined automatically by the game.

???- example "Example Code"
    This code loads a string that was stored in the "saveX.dat" file, if it exists, and converts it into a table using JSON.

    ```lua
    local yourMod = RegisterMod("someMod", 1)
    local json = require("json")
    -- ...
    function yourMod:OnGameStart(isSave)
    	--Loading Moddata--
    	if yourMod:HasData() then
    		local myTable = json.decode(yourMod:LoadData())
    	end
    end
    yourMod:AddCallback(ModCallbacks.MC_POST_GAME_STARTED, yourMod.OnGameStart)

    ```

___
### Remove·Callback () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void RemoveCallback ( int callbackId, function callbackFn ) {: .copyable aria-label='Functions' }

___
### Remove·Data () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void RemoveData ( ) {: .copyable aria-label='Functions' }

Deletes the stored "saveX.dat" file if it exists.
There are 3 "saveX.dat" files, one per Savegame. They are stored in the mod's folder next to the "main.lua" file. The number indicates the savegame it corresponds to. The number will be determined automatically by the game.
___
### Save·Data () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SaveData ( string data ) {: .copyable aria-label='Functions' }

- Stores a string in a "saveX.dat" file. The stored data persists between runs and between game launches.
- The filename will be either "save1.dat", "save2.dat", or "save3.dat", depending on which save file slot the user is playing on.
- The file will be located in the "data" directory. For example: `C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\data\foo\save1.dat`
- Since mods will often have to store more than a single variable, it is recommended to store all persistent variables for your mod in a Lua table, and then convert the table to a JSON string before using this function.

???- example "Example Code"
    This code uses JSON to convert a table into a string, and saves it in the "saveX.dat" file.
    ```lua
    local json = require("json")

    local mod = RegisterMod("myMod", 1)

    local persistentData = {
      foo = 1,
      bar = 2,
    }

    function mod:preGameExit()
      local jsonString = json.encode(persistentData)
      mod:SaveData(jsonString)
    end

    mod:AddCallback(ModCallbacks.MC_PRE_GAME_EXIT, yourMod.preGameExit)
    ```

- Note that for security reasons, the game only allows you to write data to these three files. If you want to write data to arbitrary files, you have to use the `--luadebug` flag, which will enable the Lua standard library.
___
## Variables
### Name {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string Name  {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "AddCallback",
    "signature": "void AddCallback ( [ModCallbacks](enums/ModCallbacks.md) callbackId, function callbackFn, int entityId ) {: .copyable aria-label='Functions' }",
    "description": "___"
  },
  {
    "method_id": "m002",
    "name": "AddPriorityCallback",
    "signature": "void AddPriorityCallback ( [ModCallbacks](enums/ModCallbacks.md) callbackId, [CallbackPriority](enums/CallbackPriority.md) priority, function callbackFn, int entityId ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "HasData",
    "signature": "boolean HasData ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "LoadData",
    "signature": "string LoadData ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "RemoveCallback",
    "signature": "void RemoveCallback ( int callbackId, function callbackFn ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "RemoveData",
    "signature": "void RemoveData ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "SaveData",
    "signature": "void SaveData ( string data ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m008",
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
    "summary": "Mod Reference 类代表通过 RegisterMod 注册的 mod 实例，提供回调注册、优先级控制与跨存档/跨游戏流程的持久化数据保存与加载功能。",
    "use_cases": [
      "注册游戏事件回调以扩展或修改游戏行为",
      "通过优先级回调控制同一回调内多个 mod 函数的执行顺序",
      "保存和读取持久化的 mod 配置或进度数据（支持 JSON）",
      "运行时移除已注册的回调或删除已保存的 mod 数据"
    ],
    "key_methods": [
      "AddCallback",
      "AddPriorityCallback",
      "SaveData",
      "LoadData"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "向指定回调 ID 添加一个常规回调函数，可限定特定实体 ID，用于响应游戏事件。",
      "use_cases": [
        "在游戏启动或特定事件发生时执行自定义逻辑",
        "为特定实体类型添加自定义行为"
      ],
      "key_methods": [
        "AddCallback",
        "AddPriorityCallback",
        "RemoveCallback"
      ]
    },
    {
      "method_id": "m002",
      "summary": "添加一个带有执行优先级的回调函数，允许 mod 指定该回调相对于其他同回调列表函数执行的先后顺序。",
      "use_cases": [
        "需要确保自己的逻辑在其他 mod 之前或之后运行时",
        "解决多个 mod 修改同一数据时的执行顺序冲突"
      ],
      "key_methods": [
        "AddPriorityCallback",
        "AddCallback",
        "RemoveCallback"
      ]
    },
    {
      "method_id": "m003",
      "summary": "检查当前 mod 是否已有通过 SaveData 保存的存档文件（saveX.dat），返回布尔值。",
      "use_cases": [
        "在加载数据前判断是否需要执行加载逻辑",
        "防止 LoadData 返回空字符串导致解析错误"
      ],
      "key_methods": [
        "HasData",
        "SaveData",
        "LoadData",
        "RemoveData"
      ]
    },
    {
      "method_id": "m004",
      "summary": "加载并返回之前由 SaveData 存储的字符串数据，若无存档文件则返回空字符串，通常配合 JSON 反序列化使用。",
      "use_cases": [
        "恢复 mod 的持久化配置或进度",
        "配合 JSON 库将字符串还原为 Lua 表"
      ],
      "key_methods": [
        "LoadData",
        "HasData",
        "SaveData"
      ]
    },
    {
      "method_id": "m005",
      "summary": "移除先前通过 AddCallback 或 AddPriorityCallback 添加的指定回调函数，停止其响应对应事件。",
      "use_cases": [
        "暂时或永久停用某个 mod 行为",
        "防止重复注册或进行回调清理"
      ],
      "key_methods": [
        "RemoveCallback",
        "AddCallback",
        "AddPriorityCallback"
      ]
    },
    {
      "method_id": "m006",
      "summary": "删除当前存档对应的持久化数据文件（saveX.dat），彻底清除已保存的 mod 数据。",
      "use_cases": [
        "重置 mod 的存档数据",
        "在 mod 卸载或初始化时清理旧数据"
      ],
      "key_methods": [
        "RemoveData",
        "SaveData",
        "HasData"
      ]
    },
    {
      "method_id": "m007",
      "summary": "将一个字符串保存到对应存档文件的 saveX.dat 中，数据持久化且跨游戏进程存在，建议先将要保存的内容转换为 JSON 字符串。",
      "use_cases": [
        "保存玩家的 mod 进度或配置",
        "在游戏退出前或其他关键时刻持久化数据"
      ],
      "key_methods": [
        "SaveData",
        "LoadData",
        "HasData",
        "RemoveData"
      ]
    },
    {
      "method_id": "m008",
      "summary": "获取本 mod 实例的名称，通常是在 RegisterMod 时指定的名字。",
      "use_cases": [
        "日志输出或调试时识别当前 mod",
        "用于构建基于 mod 名的唯一标识"
      ],
      "key_methods": [
        "Name"
      ]
    }
  ]
}
```
