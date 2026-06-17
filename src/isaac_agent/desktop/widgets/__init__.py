# PyQt6-independent constants (safe to import without GUI)
from isaac_agent.desktop._pipeline import PIPELINE_STAGES, STAGE_ID_MAP

# PyQt6-dependent widget (only import if PyQt6 is available)
try:
    from .workflow_timeline import WorkflowTimeline
except ImportError:
    WorkflowTimeline = None  # type: ignore

__all__ = ["WorkflowTimeline", "PIPELINE_STAGES", "STAGE_ID_MAP"]
