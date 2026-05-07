# Multi-LLM Configuration Guide

Isaac AI Agent 支持多个 LLM 提供商，可在启动时通过配置选择，也可按请求动态切换。

## 支持的提供商

| 提供商 | 标识符 | 需要安装 | API Key 环境变量 |
|--------|--------|---------|-----------------|
| OpenAI (GPT) | `openai` | `langchain-openai` | `OPENAI_API_KEY` |
| GLM / 智谱 / Qwen | `glm` | `langchain-community` | `GLM_API_KEY` |
| DeepSeek | `deepseek` | `langchain-openai` | `DEEPSEEK_API_KEY` |

## 快速配置

### 1. 设置环境变量

```bash
# .env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4096
```

### 2. 验证配置

```bash
make llm-config    # 查看当前 LLM 配置
python demo_llm_providers.py    # 测试所有提供商
```

## 使用方式

### 默认提供商（Agent）

```python
from isaac_agent.core.agent import MainAgent
import asyncio

agent = MainAgent()
result = asyncio.run(agent.run("创建一个自定义物品"))
```

### 指定提供商

```python
from isaac_agent.llm_factory import init_llm
from isaac_agent.core.agent import MainAgent

# DeepSeek
llm = init_llm(provider="deepseek", model="deepseek-chat")
agent = MainAgent(llm=llm)

# GLM
llm = init_llm(provider="glm", model="glm-4")
agent = MainAgent(llm=llm)
```

### REST API 按请求切换

```bash
# 使用 GLM
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_input": "创建新物品", "llm_provider": "glm", "llm_model": "glm-4"}'

# 使用 DeepSeek
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"user_input": "创建新物品", "llm_provider": "deepseek"}'
```

## 无 LLM 模式

如果未配置任何 LLM 提供商，Agent 将自动使用**关键词回退解析器**处理请求。功能完整但生成代码使用模板骨架，缺少 LLM 的语义填充。

## 提供商细节

### OpenAI
- 默认模型: `gpt-4-turbo`
- API Base: `https://api.openai.com/v1`

### GLM (智谱 AI)
- 默认模型: `glm-4`
- 需要安装: `langchain-community`

### DeepSeek
- 默认模型: `deepseek-chat`
- API Base: `https://api.deepseek.com/v1`
- 兼容 OpenAI SDK，使用 `ChatOpenAI` 类
