"""
State management for the Isaac AI Agent workflow
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


class WorkflowStage(str, Enum):
    """Workflow pipeline stages"""
    PARSE = "parse"
    RETRIEVE = "retrieve"
    GENERATE = "generate"
    VALIDATE = "validate"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class TaskDefinition:
    """Parsed task definition from natural language input"""
    original_request: str
    title: str
    description: str
    api_calls: List[str] = field(default_factory=list)
    lua_scaffolds: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0"
    dlc_version: str = "REP+"
    libraries: List[str] = field(default_factory=list)


@dataclass
class APIReference:
    """Retrieved API reference from Isaac documentation"""
    function_name: str
    category: str
    parameters: List[Dict[str, str]] = field(default_factory=list)
    return_type: str = "void"
    description: str = ""
    example_code: str = ""
    tags: List[str] = field(default_factory=list)
    versions: List[str] = field(default_factory=list)
    libraries: List[str] = field(default_factory=list)


@dataclass
class GeneratedCode:
    """Generated Lua code artifact"""
    scaffold_type: str  # e.g., "MC_POST_GAME_STARTED"
    lua_code: str
    imports: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    requires_validation: bool = True


@dataclass
class ValidationResult:
    """Lua code validation result"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    luacheck_output: str = ""


@dataclass
class AgentState:
    """
    Complete state of the Isaac AI Agent workflow
    
    This is the central state object that flows through the LangGraph pipeline,
    being updated at each stage.
    """
    # Metadata
    session_id: str
    stage: WorkflowStage = WorkflowStage.PARSE

    # Input
    user_input: str = ""

    # User preferences
    dlc_version: str = "REP+"
    libraries: List[str] = field(default_factory=list)

    # Parsed request
    task: Optional[TaskDefinition] = None

    # Retrieved references
    api_references: List[APIReference] = field(default_factory=list)
    api_context: List[str] = field(default_factory=list)
    template_matches: List[str] = field(default_factory=list)

    # Generated artifacts
    generated_code: List[GeneratedCode] = field(default_factory=list)

    # Validation
    validation_results: List[ValidationResult] = field(default_factory=list)

    # Metadata & tracking
    iterations: int = 0
    messages: List[Dict[str, str]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the workflow log"""
        self.messages.append({"role": role, "content": content})
    
    def add_error(self, error: str) -> None:
        """Record an error"""
        self.errors.append(error)
        self.stage = WorkflowStage.ERROR
    
    def is_valid_for_generation(self) -> bool:
        """Check if state is ready to proceed to code generation"""
        return (
            self.task is not None 
            and len(self.api_references) > 0
            and self.stage not in [WorkflowStage.ERROR, WorkflowStage.COMPLETE]
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization"""
        return {
            "session_id": self.session_id,
            "stage": self.stage.value,
            "user_input": self.user_input,
            "task": self.task.__dict__ if self.task else None,
            "api_references": [ref.__dict__ for ref in self.api_references],
            "api_context": self.api_context,
            "generated_code": len(self.generated_code),
            "iterations": self.iterations,
            "errors": self.errors,
        }
