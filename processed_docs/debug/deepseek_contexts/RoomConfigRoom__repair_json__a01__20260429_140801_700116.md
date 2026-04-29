# DeepSeek Context

- class: RoomConfigRoom
- stage: repair_json
- attempt: 1
- model: deepseek-v4-pro
- max_tokens: 3200
- temperature: 0
- timestamp: 2026-04-29T14:08:01.700150

## Prompt

```text
请把下面这段损坏的 JSON 文本修复为严格合法的 JSON。

要求：
1. 只输出 JSON 对象，不要任何解释。
2. 尽量保留原字段和语义，不要新增无关字段。
3. 顶层结构应为 {"class_enhancement": ..., "method_enhancements": ...}。
类名：RoomConfigRoom

损坏的 JSON：
{
  "class_enhancement": {
    "summary": "RoomConfigRoom provides read-only access to a room's configuration as defined in the room editor, including dimensions, door placements, spawn points, type identifiers, and weighting for procedural generation.",
    "use_cases": [
      "Reading room configuration data for custom room generation",
      "Determining valid door positions and room connectivity",
      "Accessing enemy spawn points and their properties",
      "Filtering rooms by stage, type, variant, or difficulty",
      "Debugging room properties during level generation"
    ],
    "key_methods": [
      "Type",
      "Variant",
      "Subtype",
      "Doors",
      "Spawns"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "Returns the room's difficulty level, typically 5, 10, 15, or 20 for special rooms; 0 means the room cannot appear naturally.",
      "use_cases": [
        "Filtering rooms by difficulty in custom generation",
        "Assigning difficulty-based rewards",
        "Ensuring only challenging rooms appear in end-game floors"
      ],
      "key_methods": [
        "Difficulty",
        "Weight",
        "StageID",
        "Type"
      ]
    },
    {
      "method_id": "m002",
      "summary": "Returns a bitmask of valid door positions using the DoorSlotFlag enum, indicating which walls can have doors.",
      "use_cases": [
        "Determining which sides of a room can connect to adjacent rooms",
        "Preventing invalid door placements in modded rooms",
        "Custom room shape and connectivity detection"
      ],
      "key_methods": [
        "Doors",
        "Shape",
        "Width",
        "Height"
      ]
    },
    {
      "method_id": "
```

## Response

```text
{
  "class_enhancement": {
    "summary": "RoomConfigRoom provides read-only access to a room's configuration as defined in the room editor, including dimensions, door placements, spawn points, type identifiers, and weighting for procedural generation.",
    "use_cases": [
      "Reading room configuration data for custom room generation",
      "Determining valid door positions and room connectivity",
      "Accessing enemy spawn points and their properties",
      "Filtering rooms by stage, type, variant, or difficulty",
      "Debugging room properties during level generation"
    ],
    "key_methods": [
      "Type",
      "Variant",
      "Subtype",
      "Doors",
      "Spawns"
    ]
  },
  "method_enhancements": [
    {
      "method_id": "m001",
      "summary": "Returns the room's difficulty level, typically 5, 10, 15, or 20 for special rooms; 0 means the room cannot appear naturally.",
      "use_cases": [
        "Filtering rooms by difficulty in custom generation",
        "Assigning difficulty-based rewards",
        "Ensuring only challenging rooms appear in end-game floors"
      ],
      "key_methods": [
        "Difficulty",
        "Weight",
        "StageID",
        "Type"
      ]
    },
    {
      "method_id": "m002",
      "summary": "Returns a bitmask of valid door positions using the DoorSlotFlag enum, indicating which walls can have doors.",
      "use_cases": [
        "Determining which sides of a room can connect to adjacent rooms",
        "Preventing invalid door placements in modded rooms",
        "Custom room shape and connectivity detection"
      ],
      "key_methods": [
        "Doors",
        "Shape",
        "Width",
        "Height"
      ]
    }
  ]
}
```
