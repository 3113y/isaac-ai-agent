# DeepSeek Context

- class: ItemConfigCostume
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:46:37.724607

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

类名：ItemConfigCostume

原始 md 文档（该类完整文档，可能已截断）：
# Class "ItemConfigCostume"

???+ info
    You can get this class by using the following function:

    * [ItemConfigItem.Costume](ItemConfig_Item.md#costume)

    ???+ example "Example Code"
        `Isaac.GetItemConfig():GetCollectible(CollectibleType.COLLECTIBLE_SAD_ONION).Costume`

## Variables
### Anm2Path {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string Anm2Path  {: .copyable aria-label='Variables' }

___
### Has·Overlay {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean HasOverlay  {: .copyable aria-label='Variables' }

___
### Has·Skin·Alt {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean HasSkinAlt  {: .copyable aria-label='Variables' }

___
### ID {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int ID  {: .copyable aria-label='Variables' }

___
### Is·Flying {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean IsFlying  {: .copyable aria-label='Variables' }

___
### Overwrite·Color {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### boolean OverwriteColor  {: .copyable aria-label='Variables' }

___
### Priority {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### int Priority  {: .copyable aria-label='Variables' }

___
### Skin·Color {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### SkinColor SkinColor  {: .copyable aria-label='Variables' }
???+ bug "Bug"
    Since it returns UserData, this function is unusable and therefore broken.

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "Anm2Path",
    "signature": "string Anm2Path  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "HasOverlay",
    "signature": "boolean HasOverlay  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "HasSkinAlt",
    "signature": "boolean HasSkinAlt  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "ID",
    "signature": "int ID  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "IsFlying",
    "signature": "boolean IsFlying  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "OverwriteColor",
    "signature": "boolean OverwriteColor  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "Priority",
    "signature": "int Priority  {: .copyable aria-label='Variables' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "SkinColor",
    "signature": "SkinColor SkinColor  {: .copyable aria-label='Variables' }",
    "description": "???+ bug \"Bug\""
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "提供道具服装配置的只读数据，包括动画路径、覆盖标志、备用皮肤、飞行状态、颜色覆盖、优先级和肤色等信息，用于 mod 中读取和判断道具的外观效果。",
    "use_cases": [
      "获取道具服装动画文件路径以进行自定义渲染或资源验证",
      "判断道具是否有覆盖图层或替代皮肤，以决定外观叠加逻辑",
      "检查道具是否赋予飞行外观，用于角色显示变化",
      "获取服装优先级，解决多个服装效果同时存在时的显示顺序",
      "读取服装标识 ID 以关联其他配置或进行比对"
    ],
    "key_methods": [
      "Anm2Path",
      "ID",
      "Priority",
      "HasOverlay",
      "SkinColor"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "返回该道具服装的动画文件路径（.anm2 文件），用于定位和加载动画资源。",
      "use_cases": [
        "获取动画文件路径以自定角色外貌渲染",
        "检查动画资源是否存在或加载特定动画"
      ],
      "key_methods": [
        "Anm2Path",
        "ID",
        "Priority"
      ]
    },
    {
      "method_id": "m002",
      "summary": "布尔值，指示服装是否包含覆盖图层（如特效叠加层）。",
      "use_cases": [
        "判断道具是否会向角色添加额外图层",
        "决定是否绘制叠加效果，避免重叠异常"
      ],
      "key_methods": [
        "HasOverlay",
        "HasSkinAlt",
        "IsFlying"
      ]
    },
    {
      "method_id": "m003",
      "summary": "布尔值，指示服装是否提供备用皮肤外观，常用于支持多种外观的道具。",
      "use_cases": [
        "检查道具是否有备选皮肤，用于皮肤切换功能",
        "确认是否需要展示皮肤选择界面"
      ],
      "key_methods": [
        "HasSkinAlt",
        "HasOverlay",
        "SkinColor"
      ]
    },
    {
      "method_id": "m004",
      "summary": "返回服装的唯一整数标识 ID，可与 Collectible 等关联进行识别。",
      "use_cases": [
        "标识和比对不同道具的服装配置",
        "作为查找或存储服装数据的键值"
      ],
      "key_methods": [
        "ID",
        "Anm2Path",
        "Priority"
      ]
    },
    {
      "method_id": "m005",
      "summary": "布尔值，表示该服装是否让角色呈现飞行状态的外观。",
      "use_cases": [
        "判断道具是否改变角色为飞行外观",
        "在角色状态变化时应用对应的飞行服装"
      ],
      "key_methods": [
        "IsFlying",
        "HasOverlay",
        "Priority"
      ]
    },
    {
      "method_id": "m006",
      "summary": "布尔值，指示服装是否会覆盖角色的原始颜色，可能影响与其他颜色效果的叠加。",
      "use_cases": [
        "决定是否允许服装改变角色颜色，避免冲突",
        "配合肤色数据实现正确的颜色修改"
      ],
      "key_methods": [
        "OverwriteColor",
        "SkinColor",
        "HasSkinAlt"
      ]
    },
    {
      "method_id": "m007",
      "summary": "返回整数优先级，用于在多个服装同时生效时决定显示哪一套，数值越高越优先。",
      "use_cases": [
        "控制服装的渲染顺序，解决多层服装叠加问题",
        "调整不同道具服装的显示优先级"
      ],
      "key_methods": [
        "Priority",
        "Anm2Path",
        "ID"
      ]
    },
    {
      "method_id": "m008",
      "summary": "返回 SkinColor 对象以获取肤色数据，但该字段因返回 UserData 而存在 bug，实际无法正常使用。",
      "use_cases": [
        "理论上用于获取肤色进行自定义颜色调整（目前不可用）"
      ],
      "key_methods": [
        "SkinColor",
        "OverwriteColor"
      ]
    }
  ]
}
```
