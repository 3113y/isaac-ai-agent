# DeepSeek Context

- class: FontRenderSettings
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:21:48.896675

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

类名：FontRenderSettings

原始 md 文档（该类完整文档，可能已截断）：
# Class "FontRenderSettings"

???+ info
    This class was added with Repentance+ and is used in the [Font:DrawString()](Font.md#drawstring) function to define special behavior when rendering a text.

    This class can be accessed by using its constructor:

    ???+ example "Example Code"
        ```lua
        local settings = FontRenderSettings()
        ```

## Constructors
### FontRenderSettings () {: aria-label='Constructors' }
[ ](#){: .repplus .tooltip .badge }
#### [FontRenderSettings](FontRenderSettings.md) FontRenderSettings ( ) {: .copyable aria-label='Constructors' }

Returns a Game object.

???- example "Example Code"
    Example usage:
    ```lua
    local settings = FontRenderSettings()
    settings:EnableAutoWrap()
    --returns true if the font settings have autowrap enabled

    ```
___
## Functions
### Enable·Auto·Wrap () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### void EnableAutoWrap ( boolean enabled ) {: .copyable aria-label='Functions' }

___
### Enable·Truncation () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### void EnableTruncation ( boolean enabled ) {: .copyable aria-label='Functions' }

___
### Get·Alignment () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### [DrawStringAlignment](enums/DrawStringAlignment.md) GetAlignment ( ) {: .copyable aria-label='Functions' }

___
### Get·Line·Height·Modifier () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### float GetLineHeightModifier ( ) {: .copyable aria-label='Functions' }

___
### Get·Max·Characters () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### int GetMaxCharacters ( ) {: .copyable aria-label='Functions' }

___
### Get·Missing·Character·Override () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### int GetMissingCharacterOverride ( ) {: .copyable aria-label='Functions' }

___
### Is·Auto·Wrap·Enabled () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### boolean IsAutoWrapEnabled ( ) {: .copyable aria-label='Functions' }

___
### Is·Truncation·Enabled () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### boolean IsTruncationEnabled ( ) {: .copyable aria-label='Functions' }

___
### Set·Alignment () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### void SetAlignment ( [DrawStringAlignment](enums/DrawStringAlignment.md) alignment ) {: .copyable aria-label='Functions' }

___
### Set·Line·Height·Modifier () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### void SetLineHeightModifier ( float value ) {: .copyable aria-label='Functions' }

___
### Set·Max·Characters () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### void SetMaxCharacters ( int maxChars ) {: .copyable aria-label='Functions' }

___
### Set·Missing·Character·Override () {: aria-label='Functions' }
[ ](#){: .repplus .tooltip .badge }
#### void SetMissingCharacterOverride ( int character ) {: .copyable aria-label='Functions' }
Sets the default character used when a character that needs to be rendered is missing. This overrides previous [Font:SetMissingCharacter()](Font.md#setmissingcharacter) settings.

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "FontRenderSettings",
    "signature": "[FontRenderSettings](FontRenderSettings.md) FontRenderSettings ( ) {: .copyable aria-label='Constructors' }",
    "description": ""
  },
  {
    "method_id": "m002",
    "name": "EnableAutoWrap",
    "signature": "void EnableAutoWrap ( boolean enabled ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m003",
    "name": "EnableTruncation",
    "signature": "void EnableTruncation ( boolean enabled ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m004",
    "name": "GetAlignment",
    "signature": "[DrawStringAlignment](enums/DrawStringAlignment.md) GetAlignment ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m005",
    "name": "GetLineHeightModifier",
    "signature": "float GetLineHeightModifier ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m006",
    "name": "GetMaxCharacters",
    "signature": "int GetMaxCharacters ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m007",
    "name": "GetMissingCharacterOverride",
    "signature": "int GetMissingCharacterOverride ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m008",
    "name": "IsAutoWrapEnabled",
    "signature": "boolean IsAutoWrapEnabled ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m009",
    "name": "IsTruncationEnabled",
    "signature": "boolean IsTruncationEnabled ( ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m010",
    "name": "SetAlignment",
    "signature": "void SetAlignment ( [DrawStringAlignment](enums/DrawStringAlignment.md) alignment ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m011",
    "name": "SetLineHeightModifier",
    "signature": "void SetLineHeightModifier ( float value ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m012",
    "name": "SetMaxCharacters",
    "signature": "void SetMaxCharacters ( int maxChars ) {: .copyable aria-label='Functions' }",
    "description": ""
  },
  {
    "method_id": "m013",
    "name": "SetMissingCharacterOverride",
    "signature": "void SetMissingCharacterOverride ( int character ) {: .copyable aria-label='Functions' }",
    "description": "Sets the default character used when a character that needs to be rendered is missing. This overrides previous [Font:SetMissingCharacter()](Font.md#setmissingcharacter) settings."
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "用于配置通过 Font:DrawString() 渲染文本时的特殊行为，例如自动换行、截断、对齐方式、行高比例、最大字符数和缺失字符替代。",
    "use_cases": [
      "精细控制文本在画面上的放置和换行",
      "自动折行显示长文本",
      "UI文本溢出时启用截断",
      "调节多行文字的行间距",
      "为缺失字符指定后备显示字符"
    ],
    "key_methods": [
      "FontRenderSettings",
      "EnableAutoWrap",
      "EnableTruncation",
      "SetAlignment",
      "SetMaxCharacters"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "构造函数，创建一个新的 FontRenderSettings 实例，用于配置字体渲染行为。",
      "use_cases": [
        "初始化渲染设置对象"
      ],
      "key_methods": [
        "FontRenderSettings",
        "EnableAutoWrap",
        "SetAlignment",
        "SetMaxCharacters"
      ]
    },
    {
      "method_id": "m002",
      "summary": "启用或禁用文本自动换行功能。",
      "use_cases": [
        "让长文本在到达边界时自动折行",
        "禁用自动换行实现单行滚动"
      ],
      "key_methods": [
        "EnableAutoWrap",
        "IsAutoWrapEnabled",
        "SetMaxCharacters"
      ]
    },
    {
      "method_id": "m003",
      "summary": "启用或禁用文本截断功能。",
      "use_cases": [
        "限制文本显示长度，超出部分截断",
        "防止UI文本溢出容器"
      ],
      "key_methods": [
        "EnableTruncation",
        "IsTruncationEnabled",
        "SetMaxCharacters"
      ]
    },
    {
      "method_id": "m004",
      "summary": "获取当前设置的文本对齐方式。",
      "use_cases": [
        "检查绘制使用的对齐模式",
        "条件渲染逻辑中判断对齐"
      ],
      "key_methods": [
        "GetAlignment",
        "SetAlignment"
      ]
    },
    {
      "method_id": "m005",
      "summary": "获取当前行高修改值。",
      "use_cases": [
        "查看当前行距调节比例"
      ],
      "key_methods": [
        "GetLineHeightModifier",
        "SetLineHeightModifier"
      ]
    },
    {
      "method_id": "m006",
      "summary": "获取当前设置的最大显示字符数。",
      "use_cases": [
        "检查文本长度限制"
      ],
      "key_methods": [
        "GetMaxCharacters",
        "SetMaxCharacters"
      ]
    },
    {
      "method_id": "m007",
      "summary": "获取当字体缺失某个字符时使用的替代字符编码。",
      "use_cases": [
        "查看当前后备字符设置"
      ],
      "key_methods": [
        "GetMissingCharacterOverride",
        "SetMissingCharacterOverride"
      ]
    },
    {
      "method_id": "m008",
      "summary": "判断自动换行是否启用。",
      "use_cases": [
        "根据换行状态决定渲染逻辑"
      ],
      "key_methods": [
        "IsAutoWrapEnabled",
        "EnableAutoWrap"
      ]
    },
    {
      "method_id": "m009",
      "summary": "判断文本截断是否启用。",
      "use_cases": [
        "根据截断状态调整UI行为"
      ],
      "key_methods": [
        "IsTruncationEnabled",
        "EnableTruncation"
      ]
    },
    {
      "method_id": "m010",
      "summary": "设置文本在绘制区域内的水平对齐方式。",
      "use_cases": [
        "实现文本居中、左对齐或右对齐",
        "通过代码动态改变标题排列"
      ],
      "key_methods": [
        "SetAlignment",
        "GetAlignment"
      ]
    },
    {
      "method_id": "m011",
      "summary": "设置行高乘数，调整多行文本的行间距。",
      "use_cases": [
        "压缩行距显示密集文本",
        "增大行距提高可读性"
      ],
      "key_methods": [
        "SetLineHeightModifier",
        "GetLineHeightModifier"
      ]
    },
    {
      "method_id": "m012",
      "summary": "设置绘制文本时允许的最大字符数。",
      "use_cases": [
        "限制文本显示长度，防止越界",
        "截断过长的玩家名称或信息"
      ],
      "key_methods": [
        "SetMaxCharacters",
        "GetMaxCharacters",
        "EnableTruncation"
      ]
    },
    {
      "method_id": "m013",
      "summary": "指定当字体缺少所需字符时使用的默认字符，该设置会覆盖 Font 级别的缺失字符设置。",
      "use_cases": [
        "为特定文本显示替代字符",
        "统一替换缺失字符为'?'或方块"
      ],
      "key_methods": [
        "SetMissingCharacterOverride",
        "GetMissingCharacterOverride"
      ]
    }
  ]
}
```
