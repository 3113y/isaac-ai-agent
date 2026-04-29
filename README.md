# 🎮 Isaac AI Agent - 《以撒的结合：忏悔》模组代码生成系统

> 一个由 AI 驱动的工作流系统，将自然语言需求自动转化为《以撒的结合：忏悔》(The Binding of Isaac: Repentance)的 Lua 模组代码。

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-0.0.26-green)
![Lua](https://img.shields.io/badge/Lua-5.1-lightblue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 目录

- [项目愿景](#项目愿景)
- [核心架构](#核心架构)
- [快速开始](#快速开始)
- [工作流详解](#工作流详解)
- [项目结构](#项目结构)
- [开发指南](#开发指南)
- [示例](#示例)

---

## 🎯 项目愿景

**Isaac AI Agent** 是一个全栈 AI 工程项目，目标是：

1. **降低模组开发门槛** - 用自然语言描述模组需求，自动生成代码
2. **RAG 驱动的代码生成** - 基于向量检索的 AI-guided 代码生成
3. **完整的工程化支持** - Docker、DevContainer、CI/CD、代码验证
4. **生产级代码质量** - 类型检查、Luacheck 验证、自动测试

**应用场景：**
- 快速原型模组功能
- 学习 Isaac API 的最佳实践
- 自动化重复的代码生成任务
- 团队协作开发复杂模组

---

## 🏗️ 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                  用户自然语言输入                          │
│          "创建一个新物品，拾起时恢复1颗红心"                │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│ PARSER (解析器)                                          │
│ ├─ 理解用户意图                                          │
│ └─ 生成结构化任务 JSON                                   │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│ RAG ENGINE (检索引擎)                                    │
│ ├─ 向量化检索相关 API                                    │
│ ├─ 查询喂血库                                            │
│ └─ 返回匹配的函数文档                                    │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│ GENERATOR (代码生成)                                     │
│ ├─ 选择合适的 Lua 框架                                   │
│ ├─ 融合 API 文档和模板                                   │
│ └─ 生成工程级 Lua 代码                                   │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│ VALIDATOR (验证器)                                       │
│ ├─ Luacheck 语法检查                                    │
│ ├─ 类型检查                                              │
│ └─ 反馈与迭代改进                                        │
└──────────────────────┬──────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│              最终生成的 Lua 模组代码                       │
│            📦 ready to load into Isaac                  │
└─────────────────────────────────────────────────────────┘
```

**技术栈：**

| 组件 | 技术 | 用途 |
|------|------|------|
| **工作流编排** | LangGraph | 状态机管理，任务流转 |
| **LLM 集成** | LangChain | OpenAI/GPT, GLM/Qwen, Deepseek 多模型支持 |
| **向量检索** | FAISS | API 文档向量化检索 |
| **代码框架** | FastAPI | HTTP API 端点 |
| **验证工具** | Luacheck | Lua 语法检查 |
| **容器化** | Docker Compose | 开发与部署环境 |

---

## 🚀 快速开始

### 1️⃣ 前置要求

- **Docker** 和 **Docker Compose** >= 2.0
- **VS Code** (可选，用于DevContainer)
- **Python** 3.11+ (本地开发)
- **uv** 包管理器

### 2️⃣ 项目初始化

```bash
# 克隆项目
git clone https://github.com/YOUR_USER/AgentTheIsaac.git
cd AgentTheIsaac

# 安装依赖
make install

# 启动开发环境
make dev-background

# 验证安装
make check
```

### 3️⃣ 第一个请求

```bash
# 在 Python 容器中
docker-compose exec python python

>>> from isaac_agent.core.agent import MainAgent
>>> agent = MainAgent()
>>> 
>>> # 运行工作流
>>> import asyncio
>>> result = asyncio.run(agent.run("创建一个新物品，拾起时恢复1颗红心"))
>>> print(result.stage)
# WorkflowStage.COMPLETE
```

### 4️⃣ 启动 API 服务

```bash
make serve
# FastAPI 服务运行于 http://localhost:8000

# 查看 API 文档
# http://localhost:8000/docs
```

### 5️⃣ (新！) 体验 Vector RAG 系统

```bash
# 运行 RAG 系统演示
make rag-demo

# 查看 RAG 系统统计
make rag-stats

# 重建向量索引
make rag-rebuild
```

详见 [RAG_SYSTEM.md](RAG_SYSTEM.md) - 完整的向量搜索系统文档

### 6️⃣ (新！) 配置多个 LLM 提供商

Isaac AI Agent 支持 **OpenAI (GPT)**、**GLM (智谱/Qwen)**、**Deepseek** 等多个 LLM 提供商。

**快速配置：**

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env，添加你的 API 密钥和选择提供商
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

**使用不同的 LLM 提供商：**

```python
# Python API
from isaac_agent.llm_factory import init_llm
from isaac_agent.core.agent import MainAgent

# 使用 Deepseek
llm = init_llm(provider="deepseek", model="deepseek-chat")
agent = MainAgent(llm=llm)
result = await agent.run("创建新物品时恢复1颗红心")
```

**REST API 中按请求选择 LLM：**

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "创建新物品时恢复1颗红心",
    "llm_provider": "glm",
    "llm_model": "glm-4"
  }'
```

详见 [MULTI_LLM.md](MULTI_LLM.md) - 完整的多 LLM 配置指南

---

## 🔄 工作流详解

### 阶段 1: 解析 (PARSE)

**输入：** 自然语言请求
```
"我想创建一个自定义敌人，它在游戏开始时出现，每秒发射一颗泪弹"
```

**处理流程：**
1. 使用 LLM 理解用户意图
2. 提取关键实体：敌人类型、触发条件、行为
3. 生成结构化任务定义

**输出：** TaskDefinition
```python
TaskDefinition(
    title="Custom Enemy Spawner",
    description="Custom enemy that fires tears",
    api_calls=["MC_POST_GAME_STARTED", "OnEntityUpdate"],
    lua_scaffolds=["CUSTOM_ENTITY", "ROOM_MODIFIER"],
)
```

---

### 阶段 2: 检索 (RETRIEVE)

**输入：** TaskDefinition 中的 API 调用

**处理流程：**
1. 向量化 API 调用名称
2. 搜索 Isaac API 向量库 (FAISS)
3. 返回匹配的函数文档和示例代码

**输出：** APIReference 列表
```python
APIReference(
    function_name="MC_POST_GAME_STARTED",
    category="Callbacks",
    description="Called after the game has started or loaded",
    example_code="...",
    parameters=[...],
)
```

---

### 阶段 3: 生成 (GENERATE)

**输入：** TaskDefinition + APIReference

**处理流程：**
1. 为每个 scaffold 获取 Lua 模板
2. 使用 LLM 填充模板参数
3. 融合 API 文档生成具体实现
4. 输出工程级代码

**输出：** GeneratedCode
```lua
-- 生成的 Lua 代码
function mod:MC_POST_GAME_STARTED(continued)
    local game = Game()
    -- ... 自动生成的模组逻辑 ...
end
```

---

### 阶段 4: 验证 (VALIDATE)

**输入：** GeneratedCode

**处理流程：**
1. Lua 语法检查 (luacheck)
2. API 调用验证
3. 依赖检查

**输出：** ValidationResult
```python
ValidationResult(
    is_valid=True,
    errors=[],
    warnings=[],
    luacheck_output="All checks passed",
)
```

---

### 阶段 5: 完成 (COMPLETE)

**输入：** 验证通过的代码

**输出：** 可直接导入 Isaac 的 Lua 文件

```bash
mods/
├── MyMod/
│   ├── main.lua
│   └── metadata.xml
└── MyMod.zip  # 可分享的模组
```

---

## 📁 项目结构

```
AgentTheIsaac/
│
├── 🔧 工程化文件
├── docker-compose.yml         # 容器编排配置
├── Dockerfile                 # Python 环境镜像
├── pyproject.toml            # 项目配置和依赖
├── Makefile                  # 开发任务自动化
│
├── 📂 .devcontainer/
│   ├── devcontainer.json     # VS Code 开发容器
│   └── post-create.sh        # 初始化脚本
│
├── 📂 src/
│   └── isaac_agent/
│       │
│       ├── __init__.py
│       │
│       ├── 🧠 core/           # 核心工作流
│       │   ├── agent.py       # MainAgent & StateGraph
│       │   ├── state.py       # AgentState 数据模型
│       │   └── __init__.py
│       │
│       ├── 🔍 tools/          # RAG 工具
│       │   ├── isaac_api_search.py  # API 检索工具
│       │   └── __init__.py
│       │
│       ├── 📋 templates/      # Lua 代码模板库
│       │   ├── lua_skeletons.py     # 模板集合
│       │   └── __init__.py
│       │
│       ├── 🌐 api/            # FastAPI 应用 [待实现]
│       │   ├── app.py
│       │   └── routes.py
│       │
│       └── 📦 utils/          # 工具函数 [待实现]
│           ├── config.py
│           └── logger.py
│
├── 📂 tests/                  # 单元测试 [待实现]
│   ├── test_parser.py
│   ├── test_retrieval.py
│   ├── test_generator.py
│   └── test_validator.py
│
├── 📂 mods/                   # 生成的模组输出
│   └── example_mod/
│       ├── main.lua
│       └── metadata.xml
│
├── 📂 examples/               # 示例和演示 [待实现]
│   ├── custom_item.py
│   ├── custom_enemy.py
│   └── event_system.py
│
├── 📄 README.md              # 此文件
├── 📄 CONTRIBUTING.md        # 贡献指南 [待实现]
└── 📄 LICENSE                # MIT License
```

---

## 🛠️ 开发指南

### 环境设置

#### 选项 1: VS Code DevContainer (推荐)

```bash
1. 安装 VS Code Dev Containers 扩展
2. Ctrl+Shift+P -> Dev Containers: Open in Container
3. 环境自动配置完毕！
```

#### 选项 2: 本地 Python 环境

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # 或 .venv\Scripts\activate (Windows)

# 安装依赖
uv sync
```

#### 选项 3: Docker 容器

```bash
make dev
```

### 常用命令

```bash
# 开发服务器
make serve                    # 启动 FastAPI

# 代码质量
make lint                     # 代码检查
make format                   # 代码格式化
make test                     # 运行单元测试

# 构建和验证
make build                    # 生成模组
make check-lua                # Lua 语法检查
make check                    # 全量检查

# 清理
make clean                    # 删除构建文件
make down                     # 停止容器
```

### 代码风格

遵循 PEP 8 标准，使用：
- **Black** 格式化 (100 字符行长)
- **Ruff** 代码检查
- **mypy** 类型检查

```bash
# 自动格式化
make format

# 检查
make lint
```

---

## 📚 示例

### 例 1: 创建自定义物品

**请求：**
```
创建一个新物品叫"红心收集器"，拾起时恢复 2 颗红心，使用时增加 5 秒防护
```

**工作流执行：**
```
PARSE   → 提取物品属性、效果
RETRIEVE → 查找 ItemPool、OnItemPickup、OnItemUse API
GENERATE → 使用 CUSTOM_ITEM 模板生成代码
VALIDATE → 检查 Lua 语法
COMPLETE → 导出 mod/CustomItem 目录
```

**生成的代码：**
```lua
local itemID = Isaac.GetItemIdByName("RedHeartCollector")

function mod:OnItemPickup(item, player)
    if item.ID == itemID then
        player:AddHearts(2)
        logger:info("Picked up RedHeartCollector")
    end
end

-- ... 更多生成的代码 ...
```

---

### 例 2: 创建房间修饰符

**请求：**
```
每次进入Boss房间时，生成3只自定义敌人在房间四角
```

**工作流执行：**
```
PARSE   → 房间类型（Boss房），敌人数量和位置
RETRIEVE → MC_POST_NEW_ROOM、EntitySpawn API
GENERATE → ROOM_MODIFIER 模板
VALIDATE → 参数检查
COMPLETE → 导出完整模组
```

---

## 🧪 测试

```bash
# 运行所有测试
make test

# 特定测试文件
pytest tests/test_parser.py -v

# 生成覆盖率报告
pytest --cov=src --cov-report=html
```

---

## 🐳 Docker 容器

### 文档处理器

一键运行文档处理器，自动分析 Isaac API 文档：

```bash
docker compose run --rm isaac-processor
```

详见 [DOCKER.md](DOCKER.md) — 完整 Docker 使用指南

### 开发环境

```bash
# 启动所有服务（后台）
docker-compose up -d

# 进入 Python 容器
docker-compose exec python bash

# 查看日志
docker-compose logs -f python

# 停止服务
docker-compose down
```

---

## 📖 API 文档

启动服务后访问：
- **交互式 API 文档** - http://localhost:8000/docs
- **OpenAPI Schema** - http://localhost:8000/openapi.json

---

## 🚀 部署

### 生产环境部署 (AWS/GCP/Azure)

```bash
# 构建镜像
docker build -t isaac-agent:latest .

# 推送到容器仓库
docker tag isaac-agent:latest myregistry/isaac-agent:latest
docker push myregistry/isaac-agent:latest

# 在 Kubernetes/ECS 中部署
kuscectl apply -f k8s/deployment.yaml
```

---

## 📋 常见问题 (FAQ)

### Q: 为什么生成的代码不能加载？
**A:** 检查 `metadata.xml` 文件格式，确保 Isaac 版本兼容。

### Q: 如何扩展 Lua 模板库？
**A:** 编辑 `src/isaac_agent/templates/lua_skeletons.py`，添加新的模板到 `TEMPLATES` 字典。

### Q: 支持哪些 Isaac 版本？
**A:** 目前针对 Repentance (1.7+)，向后兼容 Afterbirth+ 的部分 API。

### Q: 如何强制重新验证生成的代码？
**A:** 运行 `make check-lua` 或 `docker-compose run lua-validator`。

---

## 🤝 贡献指南

欢迎提交 Issue 和 PR！

```bash
# Fork 项目
# 创建分支: git checkout -b feature/amazing-feature
# 提交更改: git commit -m 'Add amazing feature'
# 推送分支: git push origin feature/amazing-feature
# 开启 Pull Request
```

**开发规范：**
- 遵循 PEP 8 代码风格
- 新功能需要单元测试
- 提交信息使用明确的英文描述
- 更新 README 文档

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🎓 学习资源

- [Isaac API 官方文档](https://wofsauge.github.io/IsaacDocs/)
- [LangChain 文档](https://python.langchain.com/)
- [LangGraph 教程](https://langchain-ai.github.io/langgraph/)
- [Lua 5.1 手册](https://www.lua.org/manual/5.1/)

---

## 📞 联系方式

- 📧 Email: dev@isaac-agent.local
- 💬 Discord: [Isaac Modding Community](https://discord.gg/isaac)
- 🐛 Issues: [GitHub Issues](https://github.com/YOUR_USER/AgentTheIsaac/issues)

---

## 🎉 致谢

感谢以下项目的灵感和支持：
- The Binding of Isaac 社区
- LangChain & LangGraph 项目
- Isaac API 文档维护者

---

**最后更新：** 2026 年 4 月 5 日  
**版本：** 0.1.0 (Alpha)

```
═══════════════════════════════════════════════════════════════
  🎮 Happy Modding! 祝各位模组开发愉快！
═══════════════════════════════════════════════════════════════
```
