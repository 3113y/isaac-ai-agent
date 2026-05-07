"""
Isaac AI Agent - A workflow-driven code generation system for The Binding of Isaac: Repentance
"""

__version__ = "0.1.0"
__author__ = "AI Architect"


def __getattr__(name):
    """Lazy imports — avoids loading heavy deps (FAISS, sentence-transformers, langchain)
    at package import time."""
    _imports = {
        "MainAgent": ("isaac_agent.core.agent", "MainAgent"),
        "AgentState": ("isaac_agent.core.state", "AgentState"),
        "IsaacAPISearchTool": ("isaac_agent.tools.vector_rag", "IsaacAPISearchTool"),
        "LuaTemplateManager": ("isaac_agent.templates.lua_skeletons", "LuaTemplateManager"),
    }
    if name in _imports:
        module_name, attr_name = _imports[name]
        import importlib
        mod = importlib.import_module(module_name)
        attr = getattr(mod, attr_name)
        globals()[name] = attr
        return attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "MainAgent",
    "AgentState",
    "IsaacAPISearchTool",
    "LuaTemplateManager",
]
