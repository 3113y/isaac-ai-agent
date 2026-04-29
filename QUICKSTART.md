# 本地运行指南

不使用 Docker，直接在本地 Python 环境中运行文档处理器。

## 前置要求

- Python 3.11+
- DeepSeek API Key（免费获取: https://platform.deepseek.com）

## 1. 安装依赖

```bash
pip install anthropic pyyaml loguru
```

## 2. 配置 API Key

```powershell
# Windows
$env:DEEPSEEK_API_KEY = "sk-xxx"
```

```bash
# Linux/Mac
export DEEPSEEK_API_KEY="sk-xxx"
```

## 3. 运行

```bash
python scripts/document_processor.py
```

## 输出

```
processed_docs/
├── processed_apis.json      # 提取的 API 数据
├── rag_knowledge_base.json  # RAG 系统知识库
└── report.json              # 处理统计报告
```

## 故障排除

| 问题 | 解决 |
|------|------|
| `未设置 DEEPSEEK_API_KEY` | 设置环境变量 |
| `ModuleNotFoundError` | `pip install anthropic pyyaml loguru` |
| `FileNotFoundError` | 确保在项目根目录运行 |

---

如需 Docker 方式运行，参见 [DOCKER.md](DOCKER.md)。
