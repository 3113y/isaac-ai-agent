# DeepSeek Context

- class: GridEntityRock
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:36:48.145446

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

类名：GridEntityRock

原始 md 文档（该类完整文档，可能已截断）：
# Class "GridEntityRock"

???+ info
    You can get this class by using the following function:

    * [GridEntity.ToRock()](GridEntity.md#torock)

    ???+ example "Example Code"
        `Game():GetRoom():GetGridEntity(25):ToRock()`

## Class Diagram
--8<-- "docs/snippets/GridEntityClassDiagram.md"
## Functions
### Get·Big·Rock·Frame () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### int GetBigRockFrame ( ) {: .copyable aria-label='Functions' }

___
### Get·Rubble·Anim () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### string GetRubbleAnim ( ) {: .copyable aria-label='Functions' }

___
### Get·Sprite () {: aria-label='Functions' }
[ ](#){: .const .tooltip .badge } [ ](#){: .alldlc .tooltip .badge }
#### const [Sprite](Sprite.md) GetSprite ( ) {: .copyable aria-label='Functions' }
Same as the Repentance exclusive function [GetSprite()](GridEntity.md#getsprite).

___
### Set·Big·Rock·Frame () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void SetBigRockFrame ( int Frame ) {: .copyable aria-label='Functions' }

___
### Update·Anim·Frame () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void UpdateAnimFrame ( ) {: .copyable aria-label='Functions' }

___
## Variables
### Anim {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string Anim  {: .copyable aria-label='Variables' }

___
### Frame·Cnt {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int FrameCnt  {: .copyable aria-label='Variables' }

___
### Rubble·Anim {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string RubbleAnim  {: .copyable aria-label='Variables' }

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "GetBigRockFrame",
    "signature": "int GetBigRockFrame ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "GetRubbleAnim",
    "signature": "string GetRubbleAnim ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "GetSprite",
    "signature": "const [Sprite](Sprite.md) GetSprite ( ) {: .copyable aria-label='Functions' }",
    "description": "Same as the Repentance exclusive function [GetSprite()](GridEntity.md#getsprite)."
  },
  {
    "method_id": "m004",
    "name": "SetBigRockFrame",
    "signature": "void SetBigRockFrame ( int Frame ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "UpdateAnimFrame",
    "signature": "void UpdateAnimFrame ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "Anim",
    "signature": "string Anim  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "FrameCnt",
    "signature": "int FrameCnt  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "RubbleAnim",
    "signature": "string RubbleAnim  {: .copyable aria-label='Variables' }",
    "description": ""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "表示网格中的岩石实体，提供动画状态和视觉表现的控制，支持普通岩石与大岩石的帧管理、瓦砾动画等。",
    "use_cases": [
      "获取岩石当前动画帧以同步特效或逻辑",
      "设置大岩石的动画帧来控制破坏过程",
      "手动更新岩石动画以实现自定义节奏",
      "根据瓦砾动画字符串决定岩石破碎后的外观",
      "通过精灵对象修改岩石的渲染行为"
    ],
    "key_methods": [
      "GetBigRockFrame",
      "SetBigRockFrame",
      "UpdateAnimFrame",
      "GetRubbleAnim",
      "GetSprite"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "返回当前大岩石的动画帧索引，用于同步动画状态或判断特定帧。",
      "use_cases": [
        "检测大岩石是否到达断裂关键帧",
        "配合其他实体根据帧数播放音效"
      ],
      "key_methods": [
        "GetBigRockFrame",
        "SetBigRockFrame",
        "UpdateAnimFrame",
        "FrameCnt"
      ]
    },
    {
      "method_id": "m002",
      "summary": "返回当前瓦砾动画的名称字符串，表示岩石被破坏后残留物的动画类型。",
      "use_cases": [
        "根据瓦砾动画决定后续生成物的样式",
        "在脚本中根据动画名禁用或启用碰撞"
      ],
      "key_methods": [
        "GetRubbleAnim",
        "RubbleAnim",
        "Anim"
      ]
    },
    {
      "method_id": "m003",
      "summary": "获取该岩石精灵的只读 Sprite 对象，用于精细控制渲染或动画替换。",
      "use_cases": [
        "覆盖岩石的默认精灵来源",
        "同步外部特效与岩石的动画位置"
      ],
      "key_methods": [
        "GetSprite",
        "UpdateAnimFrame",
        "Anim"
      ]
    },
    {
      "method_id": "m004",
      "summary": "将大岩石的动画帧设置为指定值，用于跳转或重置动画进度。",
      "use_cases": [
        "播放岩石碎裂的关键帧序列",
        "重置动画以循环表现特殊状态"
      ],
      "key_methods": [
        "SetBigRockFrame",
        "GetBigRockFrame",
        "UpdateAnimFrame",
        "FrameCnt"
      ]
    },
    {
      "method_id": "m005",
      "summary": "手动推进一帧岩石的动画，用于自定义更新循环中控制动画速度。",
      "use_cases": [
        "在暂停菜单外保持动画同步",
        "实现慢动作或快进效果"
      ],
      "key_methods": [
        "UpdateAnimFrame",
        "GetBigRockFrame",
        "SetBigRockFrame",
        "FrameCnt",
        "GetSprite"
      ]
    },
    {
      "method_id": "m006",
      "summary": "字符串属性，表示岩石当前使用的主体动画名称（如普通、大岩石等）。",
      "use_cases": [
        "获取或更改岩石的动画集",
        "判断岩石当前处于何种形态"
      ],
      "key_methods": [
        "Anim",
        "GetSprite",
        "RubbleAnim",
        "UpdateAnimFrame"
      ]
    },
    {
      "method_id": "m007",
      "summary": "整数属性，保存当前动画的时间计数器，与帧推进相关。",
      "use_cases": [
        "读取或修改动画播放进度",
        "配合自定义动画速度使用"
      ],
      "key_methods": [
        "FrameCnt",
        "UpdateAnimFrame",
        "GetBigRockFrame"
      ]
    },
    {
      "method_id": "m008",
      "summary": "字符串属性，存储岩石被破坏后瓦砾的动画名称。",
      "use_cases": [
        "决定岩石破碎后的视觉表现",
        "根据瓦砾类型触发不同掉落"
      ],
      "key_methods": [
        "RubbleAnim",
        "GetRubbleAnim",
        "Anim"
      ]
    }
  ]
}
```
