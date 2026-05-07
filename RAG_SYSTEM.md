# RAG System — Vector Search for Isaac API

Isaac AI Agent 使用 **FAISS 向量检索引擎** 从 1,557 条 Isaac API 文档中检索最相关的函数、回调和参数信息，为 LLM 代码生成提供上下文。

## 架构

```
用户查询 → 向量化(HuggingFace Embeddings) → FAISS 索引 → Top-K 结果 → Agent 上下文注入
```

### 核心组件

| 组件 | 模块 | 说明 |
|------|------|------|
| `VectorRAG` | `tools/vector_rag.py` | FAISS 向量搜索核心，支持 HuggingFace / OpenAI 嵌入 |
| `RAGBridge` | `tools/rag_bridge.py` | 知识库桥接层，将 `rag_knowledge_base.json` 接入 VectorRAG |
| `KnowledgeBaseLoader` | `tools/rag_bridge.py` | 加载和格式化知识库条目 |
| `IsaacAPIDatabase` | `tools/vector_rag.py` | 内置 30+ 条目回退数据库 |

## 数据流

```
processed_docs/rag_knowledge_base.json (1,557 条)
    ↓ KnowledgeBaseLoader.format_documents()
文档文本 + 元数据对
    ↓ VectorRAG._build_index()
FAISS 向量索引 (data/isaac_api.faiss)
    ↓ RAGBridge.search(query, top_k=5)
Agent 上下文注入
```

## 使用方式

### CLI 演示

```bash
make rag-demo        # 交互式搜索
make rag-stats       # 查看统计信息
make rag-rebuild     # 重建 FAISS 索引
```

### Python API

```python
from isaac_agent.tools.rag_bridge import RAGBridge

bridge = RAGBridge()

# 搜索 API
results = bridge.search("player health modification", top_k=5)
for r in results:
    print(f"{r['function']}: {r['description']}")

# 获取 Agent 提示词上下文
context = bridge.get_context_for_agent("AddHearts")
```

### 索引重建

知识库更新后需要重建索引：

```python
bridge = RAGBridge()
bridge.rebuild_index()
```

## 嵌入模型

| 模型 | 说明 |
|------|------|
| `huggingface` (默认) | 本地运行，基于 sentence-transformers |
| `openai` | 需设置 `OPENAI_API_KEY` |

## 索引文件

- 路径: `data/isaac_api.faiss`
- 可通过 `FAISS_INDEX_PATH` 环境变量自定义
- 首次初始化会自动构建
