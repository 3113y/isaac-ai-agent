# Contributing Guide

## 开发环境

```bash
uv sync --extra dev
uv run pytest tests/ -v
```

## 项目架构

```
src/isaac_agent/
    core/       # LangGraph 工作流编排
    tools/      # RAG 检索、知识库桥接
    templates/  # Lua 模板库
    api.py      # FastAPI 应用
    build.py    # Mod 输出构建器
    llm_factory.py  # LLM 提供商工厂
    config.py   # pydantic-settings 配置
```

## 工作流

`PARSE → RETRIEVE → GENERATE → VALIDATE → (regenerate or COMPLETE)`

## 编码规范

- **格式化**: Black (line-length=100), Ruff
- **类型检查**: mypy
- **测试**: pytest + pytest-asyncio
- **Python**: 3.11+

### 提交信息格式

```
<type>: <description>
```

Type: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

## 运行测试

```bash
uv run pytest tests/ -v -o "addopts="
```

## 添加新模板

编辑 `src/isaac_agent/templates/lua_skeletons.py`:

```python
TEMPLATES = {
    # ... 现有模板 ...
    "MY_TEMPLATE": '''-- 你的 Lua 模板代码''',
}
```
