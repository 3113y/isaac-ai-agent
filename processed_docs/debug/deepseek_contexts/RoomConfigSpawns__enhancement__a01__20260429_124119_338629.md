# DeepSeek Context

- class: RoomConfigSpawns
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T12:41:19.338669

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

类名：RoomConfigSpawns

原始 md 文档（该类完整文档，可能已截断）：
# Class "RoomConfigSpawns"

???+ info
    You can get this class by using the following function:

    * [RoomConfigRoom.Spawns](RoomConfig_Room.md#spawns)

    ???+ example "Example Code"
        ```lua
        local level = Game():GetLevel()
        local roomDescriptor = level:GetCurrentRoomDesc()
        local roomConfigRoom = roomDescriptor.Data
        local spawnList = roomConfigRoom.Spawns
        ```

## Operators
### __len () {: aria-label='Operators' }
[ ](#){: .alldlc .tooltip .badge }
#### int __len ( ) {: .copyable aria-label='Operators' }

The length (#) operation. Returns the amount of spawnables in this list.

___
## Functions
### Get () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### [RoomConfig Spawn](RoomConfig_Spawn.md) Get ( int idx ) {: .copyable aria-label='Functions' }

Returns a [RoomConfig Spawn](RoomConfig_Spawn.md) at the index of the list provided.

___
## Variables
### Size {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int Size  {: .copyable aria-label='Variables' }

The amount of spawnables in the list.

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "__len",
    "signature": "int __len ( ) {: .copyable aria-label='Operators' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "Get",
    "signature": "[RoomConfig Spawn](RoomConfig_Spawn.md) Get ( int idx ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "Size",
    "signature": "const int Size  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "管理房间配置中所有可生成物（Spawn）的列表，提供数量查询和按索引获取具体生成物对象的功能。",
    "use_cases": [
      "获取房间内预计生成的敌人、道具等总数",
      "遍历所有生成物以创建或配置实体",
      "根据索引检查特定生成物的类型和位置"
    ],
    "key_methods": [
      "__len",
      "Get",
      "Size"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "获取列表中可生成物的总数，对应于长度操作符（#），返回值与 Size 变量相同。",
      "use_cases": [
        "在循环开始前获取总数量",
        "快速判断列表是否为空"
      ],
      "key_methods": [
        "__len",
        "Get",
        "Size"
      ]
    },
    {
      "method_id": "m002",
      "summary": "根据提供的整数索引从列表中返回一个 RoomConfigSpawn 对象，用于获取该生成物的详细配置数据。",
      "use_cases": [
        "遍历所有生成物并获取每个生成物的具体信息",
        "按索引访问特定的生成物点"
      ],
      "key_methods": [
        "Get",
        "__len",
        "Size"
      ]
    },
    {
      "method_id": "m003",
      "summary": "常量整数属性，表示列表中可生成物的数量，功能等同于 __len 运算符的返回值。",
      "use_cases": [
        "直接读取生成物总数而不调用运算符",
        "作为只读值存储或比较"
      ],
      "key_methods": [
        "Size",
        "__len",
        "Get"
      ]
    }
  ]
}
```
