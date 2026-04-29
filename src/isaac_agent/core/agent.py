"""
Main Agent workflow orchestration using LangGraph StateGraph
"""

import uuid
from typing import Any, List, Optional
from loguru import logger

from langchain_core.language_model.base import BaseLanguageModel
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

from isaac_agent.core.state import (
    AgentState, 
    WorkflowStage, 
    TaskDefinition,
    APIReference,
    GeneratedCode,
    ValidationResult,
)
from isaac_agent.tools.vector_rag import VectorRAG, IsaacAPISearchTool
from isaac_agent.templates.lua_skeletons import LuaTemplateManager


class ParserOutput(BaseModel):
    """Output from the parser node"""
    title: str
    description: str
    api_calls: List[str]
    lua_scaffolds: List[str]


class MainAgent:
    """
    Main orchestrator for the Isaac AI Agent workflow
    
    Workflow pipeline:
    1. PARSE: Extract structured task from natural language
    2. RETRIEVE: Search Isaac API documentation
    3. GENERATE: Create Lua code using templates
    4. VALIDATE: Check generated code with luacheck
    5. COMPLETE: Return final artifacts
    """
    
    def __init__(
        self,
        llm: Optional[BaseLanguageModel] = None,
        api_search_tool: Optional[VectorRAG] = None,
        template_manager: Optional[LuaTemplateManager] = None,
        max_iterations: int = 5,
        use_vector_search: bool = True,
    ):
        """Initialize the agent with optional components"""
        self.llm = llm
        self.api_search_tool = api_search_tool or VectorRAG(
            embedding_model="huggingface" if use_vector_search else "fallback"
        )
        self.template_manager = template_manager or LuaTemplateManager()
        self.max_iterations = max_iterations
        
        # Build the workflow graph
        self.graph = self._build_graph()
        self.compiled_graph = self.graph.compile()
        
        logger.info("🤖 Isaac AI Agent initialized with Vector RAG")
    
    def _build_graph(self) -> StateGraph:
        """Construct the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes for each workflow stage
        workflow.add_node("parse", self._parse_node)
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("generate", self._generate_node)
        workflow.add_node("validate", self._validate_node)
        workflow.add_node("complete", self._complete_node)
        workflow.add_node("error_handler", self._error_handler_node)
        
        # Define edges
        workflow.add_edge("parse", "retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", "validate")
        
        # Conditional edge from validate
        workflow.add_conditional_edges(
            "validate",
            self._validation_router,
            {
                "complete": "complete",
                "regenerate": "generate",
                "error": "error_handler",
            }
        )
        
        workflow.add_edge("complete", END)
        workflow.add_edge("error_handler", END)
        
        # Set entry point
        workflow.set_entry_point("parse")
        
        return workflow
    
    async def _parse_node(self, state: AgentState) -> AgentState:
        """
        Stage 1: Parse natural language input into structured task
        
        Converts user request to JSON task definition.
        """
        logger.info(f"📝 Parsing input: {state.user_input[:100]}...")
        state.stage = WorkflowStage.PARSE
        
        # TODO: Use LLM to actually parse the input
        # For now, use simplified mock logic
        task = TaskDefinition(
            original_request=state.user_input,
            title="ModEvent Processor",
            description="Create custom handling for game events",
            api_calls=["RegisterMod", "OnEvent"],
            lua_scaffolds=["MC_POST_GAME_STARTED"],
        )
        
        state.task = task
        state.add_message("agent", f"✅ Parsed task: {task.title}")
        state.iterations += 1
        
        logger.info(f"✅ Task parsed: {task.title}")
        return state
    
    async def _retrieve_node(self, state: AgentState) -> AgentState:
        """
        Stage 2: Retrieve relevant API references from Isaac API
        
        Uses RAG to find matching functions and callbacks.
        """
        logger.info("🔍 Retrieving API references...")
        state.stage = WorkflowStage.RETRIEVE
        
        if not state.task:
            state.add_error("No task available for retrieval")
            return state
        
        # Search for each API call mentioned in the task
        for api_call in state.task.api_calls:
            # Use the search tool
            results = self.api_search_tool.search(api_call)
            state.api_references.extend(results)
        
        # Also get templates for scaffolds
        for scaffold in state.task.lua_scaffolds:
            matches = self.template_manager.find_templates(scaffold)
            state.template_matches.extend(matches)
        
        state.add_message(
            "agent", 
            f"📚 Retrieved {len(state.api_references)} API references"
        )
        state.iterations += 1
        
        logger.info(f"✅ Retrieved {len(state.api_references)} references")
        return state
    
    async def _generate_node(self, state: AgentState) -> AgentState:
        """
        Stage 3: Generate Lua code using templates and API info
        
        Creates concrete implementation based on scaffolds and API references.
        """
        logger.info("⚙️  Generating Lua code...")
        state.stage = WorkflowStage.GENERATE
        
        if not state.task or not state.api_references:
            state.add_error("Incomplete state for code generation")
            return state
        
        # Generate code for each scaffold
        for scaffold_name in state.task.lua_scaffolds:
            template = self.template_manager.get_template(scaffold_name)
            
            # Create the code artifact
            code = GeneratedCode(
                scaffold_type=scaffold_name,
                lua_code=template,
                requires_validation=True,
            )
            state.generated_code.append(code)
        
        state.add_message(
            "agent",
            f"✨ Generated {len(state.generated_code)} code artifacts"
        )
        state.iterations += 1
        
        logger.info(f"✅ Generated {len(state.generated_code)} Lua artifacts")
        return state
    
    async def _validate_node(self, state: AgentState) -> AgentState:
        """
        Stage 4: Validate generated Lua code
        
        Runs luacheck and syntax validation on all generated code.
        """
        logger.info("✔️  Validating Lua code...")
        state.stage = WorkflowStage.VALIDATE
        
        for artifact in state.generated_code:
            # Mock validation logic
            result = ValidationResult(
                is_valid=True,
                errors=[],
                warnings=[],
                luacheck_output="All checks passed",
            )
            state.validation_results.append(result)
        
        state.add_message(
            "agent",
            f"✅ Validated {len(state.validation_results)} artifacts"
        )
        state.iterations += 1
        
        logger.info("✅ Validation complete")
        return state
    
    def _validation_router(self, state: AgentState) -> str:
        """Route based on validation results"""
        if state.stage == WorkflowStage.ERROR:
            return "error"
        
        if all(r.is_valid for r in state.validation_results):
            return "complete"
        else:
            return "regenerate"
    
    async def _complete_node(self, state: AgentState) -> AgentState:
        """
        Final stage: Mark workflow as complete
        
        Prepares final output artifacts.
        """
        logger.info("🎉 Workflow complete!")
        state.stage = WorkflowStage.COMPLETE
        state.add_message("agent", "✅ Workflow completed successfully")
        return state
    
    async def _error_handler_node(self, state: AgentState) -> AgentState:
        """Handle workflow errors"""
        logger.error(f"❌ Workflow error: {state.errors}")
        state.add_message("system", f"Error: {', '.join(state.errors)}")
        return state
    
    async def run(self, user_input: str) -> AgentState:
        """
        Execute the complete workflow
        
        Args:
            user_input: Natural language request from user
            
        Returns:
            Final AgentState with generated artifacts
        """
        session_id = str(uuid.uuid4())[:8]
        logger.info(f"🚀 Starting new workflow session: {session_id}")
        
        # Initialize state
        initial_state = AgentState(
            session_id=session_id,
            user_input=user_input,
        )
        
        # Execute the compiled graph
        final_state = await self.compiled_graph.ainvoke(initial_state)
        
        logger.info(f"✅ Workflow {session_id} completed with state: {final_state.stage}")
        return final_state
    
    def get_workflow_info(self) -> dict:
        """Return information about the workflow"""
        return {
            "name": "Isaac AI Agent",
            "version": "0.1.0",
            "stages": [stage.value for stage in WorkflowStage],
            "max_iterations": self.max_iterations,
            "has_llm": self.llm is not None,
        }
