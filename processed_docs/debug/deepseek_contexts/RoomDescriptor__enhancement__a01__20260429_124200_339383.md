# DeepSeek Context

- class: RoomDescriptor
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T12:42:00.339418

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

类名：RoomDescriptor

原始 md 文档（该类完整文档，可能已截断）：
# Class "RoomDescriptor"

???+ info
    You can get this class by using the following function:

    * [Level.GetCurrentRoomDesc](Level.md#getcurrentroomdesc)
    * [Level.GetLastRoomDesc](Level.md#getlastroomdesc)
    * [Level.GetRoomByIdx](Level.md#getroombyidx)

    ???+ example "Example Code"
        ```lua
        local level = Game():GetLevel()
        local roomDescriptor = level:GetCurrentRoomDesc()
        ```

## Operators
### __len () {: aria-label='Operators' }
[ ](#){: .alldlc .tooltip .badge }
#### int __len ( ) {: .copyable aria-label='Operators' }

The length (#) operation. Returns the amount of rooms in the list.

___
## Functions
### Get () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### [RoomDescriptor](RoomDescriptor.md) Get ( int idx ) {: .copyable aria-label='Functions' }

Returns a [RoomDescriptor](RoomDescriptor.md) at the index of the list provided.

___
## Variables
### Size {: aria-label='Variables' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const int Size  {: .copyable aria-label='Variables' }

The amount of rooms in the list.

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
    "signature": "[RoomDescriptor](RoomDescriptor.md) Get ( int idx ) {: .copyable aria-label='Functions' }",
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
    "summary": "一个持有房间描述符列表的容器类，通常通过 Level 相关方法获取，用于遍历或访问当前楼层或指定列表中的房间信息。",
    "use_cases": [
      "遍历当前楼层的所有房间描述符",
      "获取指定索引的房间描述符以查询房间属性",
      "获取列表中房间的总数量"
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
      "summary": "返回房间列表中房间的数量，重载长度运算符 (#)，使实例可以直接使用 # 获取大小。",
      "use_cases": [
        "快速获取房间总数用于循环条件",
        "在判断流程中检查房间列表是否为空"
      ],
      "key_methods": [
        "__len",
        "Size"
      ]
    },
    {
      "method_id": "m002",
      "summary": "根据提供的索引返回房间列表中对应位置的单个房间描述符，索引从0开始。",
      "use_cases": [
        "遍历房间列表时按索引获取房间对象",
        "访问特定位置的房间以获取其布局、类型等信息"
      ],
      "key_methods": [
        "Get",
        "__len",
        "Size"
      ]
    },
    {
      "method_id": "m003",
      "summary": "只读属性，表示列表中房间的数量，与 __len 运算符返回值相同。",
      "use_cases": [
        "直接读取房间总数而无需调用运算符",
        "在需要明确代码可读性的上下文中使用"
      ],
      "key_methods": [
        "Size",
        "__len"
      ]
    }
  ]
}
```
