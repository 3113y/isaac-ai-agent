"""Core modules for Isaac AI Agent"""


def __getattr__(name):
    _imports = {
        "AgentState": ("isaac_agent.core.state", "AgentState"),
        "WorkflowStage": ("isaac_agent.core.state", "WorkflowStage"),
        "TaskDefinition": ("isaac_agent.core.state", "TaskDefinition"),
        "APIReference": ("isaac_agent.core.state", "APIReference"),
        "GeneratedCode": ("isaac_agent.core.state", "GeneratedCode"),
        "ValidationResult": ("isaac_agent.core.state", "ValidationResult"),
        "MainAgent": ("isaac_agent.core.agent", "MainAgent"),
    }
    if name in _imports:
        import importlib
        module_name, attr_name = _imports[name]
        mod = importlib.import_module(module_name)
        attr = getattr(mod, attr_name)
        globals()[name] = attr
        return attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "AgentState",
    "WorkflowStage",
    "TaskDefinition",
    "APIReference",
    "GeneratedCode",
    "ValidationResult",
    "MainAgent",
]
