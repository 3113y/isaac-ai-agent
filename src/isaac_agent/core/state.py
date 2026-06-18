"""
State management for the Isaac AI Agent workflow
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum


class WorkflowStage(str, Enum):
    """Workflow pipeline stages"""
    PARSE = "parse"
    PLAN = "plan"
    RETRIEVE = "retrieve"
    RETRIEVE_FILE = "retrieve_file"
    GENERATE = "generate"
    GENERATE_FILE = "generate_file"
    XML_GENERATE = "xml_generate"
    VALIDATE = "validate"
    COMPLETE = "complete"
    ASSEMBLE = "assemble"
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
class FilePlan:
    """Planned file in the generated mod's directory structure."""
    relative_path: str                             # e.g., "scripts/items/my_item.lua"
    role_description: str                          # What this file does in the mod
    required_apis: List[str] = field(default_factory=list)  # APIs this file needs
    dependencies: List[str] = field(default_factory=list)   # Other files it depends on
    template_hint: str = ""                        # Which reference file to use as pattern
    is_xml: bool = False                           # True for XML content files
    scaffold_type: str = ""                        # Architectural pattern id


@dataclass
class ModComponent:
    """A functional component in the mod (passive item, active item, etc.)"""
    component_type: str                            # "passive_item", "active_item", "familiar", etc.
    name: str                                      # e.g., "Damage Doubler"
    description: str                               # What this component does


@dataclass
class GeneratedCode:
    """Generated Lua code artifact"""
    scaffold_type: str  # e.g., "MC_POST_GAME_STARTED"
    lua_code: str
    file_path: str = ""                    # Relative path within the mod directory
    role_description: str = ""             # From the FilePlan
    imports: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    requires_validation: bool = True


@dataclass
class XmlAttribute:
    """Describes a single attribute of an XML element from schema docs"""
    name: str
    type: str = "string"
    possible_values: List[str] = field(default_factory=list)
    description: str = ""
    required: bool = False


@dataclass
class XmlSubElement:
    """Describes a nested child element within an XML file schema"""
    name: str
    attributes: List["XmlAttribute"] = field(default_factory=list)
    description: str = ""


@dataclass
class XmlFileSchema:
    """Parsed schema for one XML file type in the Isaac modding API"""
    filename: str
    root_element: str
    root_attributes: Dict[str, str] = field(default_factory=dict)
    folder: str = "unknown"
    attributes: List[XmlAttribute] = field(default_factory=list)
    sub_elements: List[XmlSubElement] = field(default_factory=list)
    tags: List[Dict[str, str]] = field(default_factory=list)
    xml_examples: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class XmlEntry:
    """A single entry to be written into an XML file"""
    element_tag: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    sub_elements: List["XmlEntry"] = field(default_factory=list)


@dataclass
class GeneratedXml:
    """Output of the XML generation stage"""
    scaffold_type: str
    xml_file: str
    folder: str = "content"
    entries: List[XmlEntry] = field(default_factory=list)
    generated_by: str = "programmatic"


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

    # Architecture planning
    file_plans: List[FilePlan] = field(default_factory=list)
    current_file_index: int = 0
    mod_components: List[ModComponent] = field(default_factory=list)
    all_files_generated: bool = False
    shared_context: str = ""  # Shared Mod_Data structure injected across files

    # Retrieved references
    api_references: List[APIReference] = field(default_factory=list)
    api_context: List[str] = field(default_factory=list)
    template_matches: List[str] = field(default_factory=list)

    # Generated artifacts
    generated_code: List[GeneratedCode] = field(default_factory=list)

    # Validation
    validation_results: List[ValidationResult] = field(default_factory=list)

    # XML generation
    generated_xml: List[Any] = field(default_factory=list)

    # Metadata & tracking
    iterations: int = 0
    file_iterations: int = 0  # Retries for the current file
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
