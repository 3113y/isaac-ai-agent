# DeepSeek Context

- class: GridEntityPressurePlate
- stage: enhancement
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 2600
- temperature: 0.2
- timestamp: 2026-04-29T13:35:40.036119

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

类名：GridEntityPressurePlate

原始 md 文档（该类完整文档，可能已截断）：
# Class "GridEntityPressurePlate"

???+ info
    You can get this class by using the following function:

    * [GridEntity.ToPressurePlate()](GridEntity.md#topressureplate)

    ???+ example "Example Code"
        `Game():GetRoom():GetGridEntity(25):ToPressurePlate()`

## Class Diagram
--8<-- "docs/snippets/GridEntityClassDiagram.md"
## Functions
### Reward () {: aria-label='Functions' }
[ ](#){: .alldlc .tooltip .badge }
#### void Reward ( ) {: .copyable aria-label='Functions' }
Triggers the spawning of the reward as if the plate would be pressed, without actually pressing it.

???- info "Greed mode behavior"
    When in greedmode and used on the Greedmode-pressureplate, it has multiple effects:

    When no wave is active, it will spawn a random reward analog to the normal pressure plate pool.

    When a wave is active, it will spawn a wave, wihtout increasing the wave counter.

___
## Variables
### Greed·Mode·RNG {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [RNG](RNG.md) GreedModeRNG {: .copyable aria-label='Variables' }
RNG object that determines the RNG of anything GreedMode related.

___
### Next·Greed·Animation {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### string NextGreedAnimation  {: .copyable aria-label='Variables' }
Defines the animation that the greed-mode pressureplate should play. This effect is only visual!

Every Animation defined in the "grid_pressureplate.anm2" file can be used as an input. Any other input will crash the game!

___
### Timer·Plate {: aria-label='Variables' }
[ ](#){: .alldlc .tooltip .badge }
#### [Sprite](Sprite.md) TimerPlate  {: .copyable aria-label='Variables' data-altreturn='nil' }
Reference to the Sprite of the Timerplate beneath the pressureplate in Greed mode.

___

方法列表（JSON）：
[
  {
    "method_id": "m001",
    "name": "Reward",
    "signature": "void Reward ( ) {: .copyable aria-label='Functions' }",
    "description": "Triggers the spawning of the reward as if the plate would be pressed, without actually pressing it."
  },
  {
    "method_id": "m002",
    "name": "GreedModeRNG",
    "signature": "[RNG](RNG.md) GreedModeRNG {: .copyable aria-label='Variables' }",
    "description": "RNG object that determines the RNG of anything GreedMode related."
  },
  {
    "method_id": "m003",
    "name": "NextGreedAnimation",
    "signature": "string NextGreedAnimation  {: .copyable aria-label='Variables' }",
    "description": "Defines the animation that the greed-mode pressureplate should play. This effect is only visual!"
  },
  {
    "method_id": "m004",
    "name": "TimerPlate",
    "signature": "[Sprite](Sprite.md) TimerPlate  {: .copyable aria-label='Variables' data-altreturn='nil' }",
    "description": "Reference to the Sprite of the Timerplate beneath the pressureplate in Greed mode."
  }
]

```

## Response

```text
{
  "class_enhancement": {
    "summary": "GridEntityPressurePlate 代表游戏中的压力板网格实体，用于在被触碰或按下时触发奖励、事件或逻辑，并专门在贪婪模式下管理相关行为和视觉效果。",
    "use_cases": [
      "检测并响应玩家或敌人对压力板的按压",
      "在贪婪模式中控制波数、生成奖励和播放特殊动画",
      "通过直接调用 Reward 方法在不实际按压的情况下触发奖励",
      "自定义贪婪模式压力板的随机生成逻辑或动画表现"
    ],
    "key_methods": [
      "Reward",
      "GreedModeRNG",
      "NextGreedAnimation",
      "TimerPlate"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "立即触发压力板的奖励生成效果，如同被按压，但不会改变按压状态。在贪婪模式下，该方法会根据当前波次状态生成随机奖励或直接激活一波敌人而不增加波数计数器。",
      "use_cases": [
        "在脚本中模拟玩家踩下压力板获得奖励",
        "在不触发压力板动画或物理碰撞的情况下生成掉落物",
        "在贪婪模式中动态控制波次生成以调整难度"
      ],
      "key_methods": [
        "Reward",
        "GreedModeRNG"
      ]
    },
    {
      "method_id": "m002",
      "summary": "获取用于控制贪婪模式所有随机行为的 RNG 对象，包括奖励生成和波次触发中的随机种子。",
      "use_cases": [
        "读取或修改贪婪模式压力板的随机种子",
        "在自定义逻辑中确保随机结果的可重现性",
        "结合 Reward 方法实现特定奖励概率控制"
      ],
      "key_methods": [
        "GreedModeRNG",
        "Reward"
      ]
    },
    {
      "method_id": "m003",
      "summary": "设置或获取贪婪压力板下一次要播放的动画名称，仅影响视觉表现，不改变实际功能。动画名称必须来自 grid_pressureplate.anm2 文件，否则会导致游戏崩溃。",
      "use_cases": [
        "在关键游戏时刻切换压力板动画以提供视觉反馈",
        "根据波次或状态显示不同的装饰动画",
        "在 Mod 中为压力板引入新动画状态"
      ],
      "key_methods": [
        "NextGreedAnimation",
        "TimerPlate",
        "Reward"
      ]
    },
    {
      "method_id": "m004",
      "summary": "返回对贪婪模式压力板下方计时器板 Sprite 对象的引用，可用于直接操作其外观、动画或属性。",
      "use_cases": [
        "调整计时器板的透明度或颜色以匹配 Mod 主题",
        "读取或设置计时器板的当前播放帧以同步视觉效果",
        "在自定义逻辑中替换计时器板的整个 Sprite"
      ],
      "key_methods": [
        "TimerPlate",
        "NextGreedAnimation",
        "Reward"
      ]
    }
  ]
}
```
