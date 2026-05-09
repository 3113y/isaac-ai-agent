"""
Main Agent workflow orchestration using LangGraph StateGraph
"""

import json
import os
import re
import subprocess
import uuid
from pathlib import Path
from typing import Any, List, Optional
from loguru import logger

from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import SystemMessage, HumanMessage
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
from isaac_agent.tools.rag_bridge import RAGBridge
from isaac_agent.templates.lua_skeletons import LuaTemplateManager
from isaac_agent.tools.isaac_path_resolver import find_isaac_mods_dir, find_isaac_log_file
from isaac_agent.tools.isaac_error_analyzer import parse_log_errors, analyze_and_suggest
from isaac_agent.config import settings


class ParserOutput(BaseModel):
    """Output from the parser node"""
    title: str
    description: str
    api_calls: List[str]
    lua_scaffolds: List[str]


def _extract_json(text: str) -> dict:
    """Extract JSON object from LLM response, handling markdown code blocks."""
    # Try parsing directly first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting from ```json ... ``` block
    match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Try extracting first { ... } block
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not extract JSON from LLM response: {text[:200]}")


def _extract_lua_code(text: str) -> str:
    """Extract Lua code from LLM response, stripping markdown fences."""
    # Strip ```lua ... ``` or ``` ... ``` blocks
    match = re.search(r'```(?:lua)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # No fences — return as-is
    return text.strip()


# ------------------------------------------------------------------
# Lua code validation (pure Python, no external dependencies)
# ------------------------------------------------------------------

# Lua keywords that start/end blocks
_LUA_BLOCK_STARTERS = {
    "function", "if", "for", "while", "do", "repeat",
}
_LUA_BLOCK_ENDERS = {
    "end", "until",
}


def _validate_lua_syntax(code: str) -> List[str]:
    """Basic Lua syntax validation. Returns list of error messages."""
    errors = []

    # Check for empty code
    if not code or not code.strip():
        errors.append("Empty code block")
        return errors

    # Count function/end balance
    lines = code.split("\n")
    block_stack = 0
    for i, line in enumerate(lines, 1):
        stripped = line.strip().split("--")[0]  # ignore comments
        words = re.findall(r'\b\w+\b', stripped)
        for w in words:
            if w in _LUA_BLOCK_STARTERS:
                block_stack += 1
            elif w in _LUA_BLOCK_ENDERS:
                block_stack -= 1
        if block_stack < 0:
            errors.append(f"Line {i}: unexpected 'end' without matching block")
            block_stack = 0

    if block_stack > 0:
        errors.append(f"Missing {block_stack} 'end' statement(s)")
    elif block_stack < 0:
        errors.append(f"Too many 'end' statements ({-block_stack})")

    # Check balanced delimiters
    delimiters = {"(": ")", "[": "]", "{": "}"}
    stack = []
    for i, ch in enumerate(code):
        if ch in delimiters:
            stack.append((ch, i))
        elif ch in delimiters.values():
            if not stack:
                errors.append(f"Char {i}: unexpected '{ch}'")
                continue
            opener, opener_pos = stack.pop()
            expected = delimiters[opener]
            if ch != expected:
                errors.append(f"Char {i}: expected '{expected}' but got '{ch}'")
    for opener, pos in stack:
        errors.append(f"Char {pos}: unclosed '{opener}'")

    # Check for RegisterMod (required for all mods)
    if "RegisterMod" not in code:
        errors.append("Missing RegisterMod call (required for mod registration)")

    return errors


def _run_luacheck(code: str) -> Optional[ValidationResult]:
    """Run luacheck on code if the binary is available. Returns None if not available."""
    luacheck_bin = os.environ.get("LUA_VALIDATOR", "luacheck")
    try:
        result = subprocess.run(
            [luacheck_bin, "--no-color", "-"],
            input=code.encode("utf-8"),
            capture_output=True,
            timeout=30,
        )
        output = result.stdout.decode("utf-8", errors="replace").strip()
        is_valid = result.returncode == 0
        errors = []
        warnings = []
        for line in output.split("\n"):
            if ": E" in line or "error" in line.lower():
                errors.append(line)
            elif ": W" in line or "warning" in line.lower():
                warnings.append(line)
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            luacheck_output=output,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return None


class MainAgent:
    """
    Main orchestrator for the Isaac AI Agent workflow

    Workflow pipeline:
    1. PARSE: Extract structured task from natural language (LLM-driven)
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
        self.template_manager = template_manager or LuaTemplateManager()
        self.max_iterations = max_iterations

        # Prefer RAGBridge (full knowledge base) over plain VectorRAG
        if api_search_tool:
            self.api_search_tool = api_search_tool
        else:
            try:
                self.api_search_tool = RAGBridge(
                    embedding_model="huggingface" if use_vector_search else "fallback",
                    use_knowledge_base=True,
                )
                logger.info("Using RAGBridge with full knowledge base")
            except (FileNotFoundError, ImportError) as e:
                logger.warning(f"Knowledge base unavailable ({e}), falling back to legacy VectorRAG")
                self.api_search_tool = VectorRAG(
                    embedding_model="huggingface" if use_vector_search else "fallback"
                )

        # Auto-detect Isaac paths (mods folder + log file)
        self._detect_paths()

        # Build the workflow graph
        self.graph = self._build_graph()
        self.compiled_graph = self.graph.compile()

        logger.info("Isaac AI Agent initialized with Vector RAG")

    def _detect_paths(self):
        """Auto-detect Isaac mods directory and log file on this machine."""
        self.mods_dir: Optional[Path] = None
        self.log_file: Optional[Path] = None

        try:
            self.mods_dir = find_isaac_mods_dir()
            if self.mods_dir:
                settings.detected_mods_dir = str(self.mods_dir)
                logger.info(f"Detected mods dir: {self.mods_dir}")
            else:
                logger.info("Mods dir not auto-detected, using default ./mods")
        except Exception as e:
            logger.warning(f"Path detection skipped (mods): {e}")

        try:
            self.log_file = find_isaac_log_file()
            if self.log_file:
                settings.detected_log_file = str(self.log_file)
                logger.info(f"Detected log file: {self.log_file}")
            else:
                logger.info("Log file not auto-detected")
        except Exception as e:
            logger.warning(f"Path detection skipped (log): {e}")

    @property
    def effective_mods_dir(self) -> Path:
        """Return the best-known mods directory (detected > config > default)."""
        if self.mods_dir and self.mods_dir.exists():
            return self.mods_dir
        configured = Path(settings.isaac_mod_dir)
        if configured.exists():
            return configured
        return Path("./mods")

    # ------------------------------------------------------------------
    # Prompt builders
    # ------------------------------------------------------------------

    def _build_parse_prompt(self, dlc_version: str = "REP+", libraries: list = None) -> str:
        """Build the system prompt for LLM-based task parsing."""
        if libraries is None:
            libraries = []
        templates = self.template_manager.list_templates()
        template_lines = "\n".join(
            f"  - {name}: {self.template_manager.get_template_description(name)}"
            for name in templates
        )
        lib_note = ""
        if libraries:
            lib_note = f"\nThe user has selected these modding libraries as dependencies: {', '.join(libraries)}. Prefer API calls that are compatible with these libraries."
        return f"""You are an expert in The Binding of Isaac: Repentance Lua modding.
Your job is to parse a user's mod request into a structured task definition.

Target DLC version: {dlc_version}. Only suggest API functions that are compatible with this version.{lib_note}

Given the user's natural language description, determine:
1. A concise title and detailed description of the mod
2. Which Isaac API functions are needed (use exact names like RegisterMod, GetPlayer, AddHearts, AddCallback, EntitySpawn, etc.)
3. Which Lua code scaffolds fit the use case

Available Lua code scaffolds:
{template_lines}

Respond with ONLY a JSON object (no markdown, no explanation):
{{
    "title": "<short descriptive title>",
    "description": "<detailed description of what the mod does>",
    "api_calls": ["Function1", "Function2", ...],
    "lua_scaffolds": ["SCAFFOLD_NAME_1", ...]
}}

Choose lua_scaffolds ONLY from the available list above. Choose api_calls using your knowledge of the Isaac modding API."""

    def _build_generation_prompt(
        self,
        scaffold_type: str,
        template: str,
        task_title: str,
        task_description: str,
        api_context: str,
        dlc_version: str = "REP+",
        libraries: list = None,
    ) -> str:
        """Build the system prompt for LLM-based Lua code generation."""
        if libraries is None:
            libraries = []
        lib_note = ""
        if libraries:
            lib_note = f"\nRequired modding libraries: {', '.join(libraries)}. Use their APIs where appropriate."
        return f"""You are an expert Lua modder for The Binding of Isaac: Repentance.
Generate complete, working Lua mod code based on the task requirements.

Target DLC version: {dlc_version}. Only use APIs compatible with {dlc_version}.{lib_note}

Task: {task_title}
Description: {task_description}

The code should follow this scaffold pattern ({scaffold_type}):

{template}

Relevant API documentation:
{api_context if api_context else "Use standard Isaac modding API patterns (RegisterMod, AddCallback, etc.)"}

Instructions:
1. Fill in the template with actual game logic that fulfills the task requirements
2. Use the API functions shown in the documentation above
3. Handle edge cases and errors appropriately
4. Add comments explaining key logic
5. Return ONLY the complete Lua code, no markdown code fences, no explanations
6. The code must be syntactically valid Lua"""

    # ------------------------------------------------------------------
    # LLM-based task parsing
    # ------------------------------------------------------------------

    async def _llm_parse(self, user_input: str, dlc_version: str = "REP+", libraries: list = None) -> TaskDefinition:
        """Use LLM to parse user input into a structured TaskDefinition."""
        if libraries is None:
            libraries = []
        messages = [
            SystemMessage(content=self._build_parse_prompt(dlc_version=dlc_version, libraries=libraries)),
            HumanMessage(content=user_input),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content if hasattr(response, 'content') else str(response)
        logger.info(f"🤖 LLM response: {raw[:200]}...")

        parsed = _extract_json(raw)
        task = TaskDefinition(
            original_request=user_input,
            title=parsed.get("title", "Untitled Mod"),
            description=parsed.get("description", user_input),
            api_calls=parsed.get("api_calls", []),
            lua_scaffolds=parsed.get("lua_scaffolds", []),
            dlc_version=dlc_version,
            libraries=libraries,
        )
        # Validate scaffolds against known templates
        valid_scaffolds = [
            s for s in task.lua_scaffolds
            if self.template_manager.validate_template(s)
        ]
        if valid_scaffolds:
            task.lua_scaffolds = valid_scaffolds
        else:
            task.lua_scaffolds = ["MOD_INIT"]

        return task

    def _fallback_parse(self, user_input: str) -> TaskDefinition:
        """Keyword-based fallback parser when LLM is unavailable."""
        user_lower = user_input.lower()

        # Map keywords to likely API calls
        api_keywords = {
            "health": ["GetPlayer", "AddHearts"],
            "heart": ["GetPlayer", "AddHearts", "AddSoulHearts"],
            "player": ["GetPlayer"],
            "item": ["GetItemIdByName", "AddItemFromPool"],
            "entity": ["EntitySpawn", "GetDescendants"],
            "enemy": ["EntitySpawn", "GetDescendants"],
            "spawn": ["EntitySpawn"],
            "tear": ["SpawnTear", "GetPlayer"],
            "room": ["GetRoom", "GetRoomData", "GetDescendants"],
            "damage": ["OnEntityTakeDamage", "GetPlayer"],
            "explosion": ["SpawnExplosion"],
            "explode": ["SpawnExplosion"],
            "pickup": ["OnItemPickup", "GetPlayer"],
            "coin": ["AddCoins"],
            "bomb": ["AddBombs"],
            "key": ["AddKeys"],
            "event": ["AddCallback", "MC_POST_GAME_STARTED"],
            "callback": ["AddCallback"],
        }
        api_calls = set()
        api_calls.add("RegisterMod")
        for keyword, funcs in api_keywords.items():
            if keyword in user_lower:
                api_calls.update(funcs)

        # Map keywords to likely scaffolds
        scaffold_keywords = {
            "item": ["CUSTOM_ITEM"],
            "entity": ["CUSTOM_ENTITY"],
            "enemy": ["CUSTOM_ENTITY"],
            "player": ["PLAYER_MODIFIER"],
            "room": ["ROOM_MODIFIER"],
            "event": ["EVENT_HANDLER"],
            "health": ["PLAYER_MODIFIER"],
            "damage": ["EVENT_HANDLER", "PLAYER_MODIFIER"],
        }
        scaffolds = set()
        for keyword, scaf in scaffold_keywords.items():
            if keyword in user_lower:
                scaffolds.update(scaf)
        if not scaffolds:
            scaffolds.add("MC_POST_GAME_STARTED")

        return TaskDefinition(
            original_request=user_input,
            title=user_input[:60],
            description=user_input,
            api_calls=list(api_calls),
            lua_scaffolds=list(scaffolds),
        )
    
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
        Stage 1: Parse natural language input into structured task.

        Uses LLM when available; falls back to keyword-based parsing.
        """
        logger.info(f"📝 Parsing input: {state.user_input[:100]}...")
        state.stage = WorkflowStage.PARSE

        if self.llm:
            try:
                task = await self._llm_parse(
                    state.user_input,
                    dlc_version=state.dlc_version,
                    libraries=state.libraries,
                )
                logger.info(f"🤖 LLM parsed: title='{task.title}', "
                            f"api_calls={task.api_calls}, scaffolds={task.lua_scaffolds}")
            except Exception as e:
                logger.warning(f"LLM parse failed ({e}), using fallback parser")
                task = self._fallback_parse(state.user_input)
        else:
            logger.info("No LLM configured, using fallback parser")
            task = self._fallback_parse(state.user_input)

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
            results = self.api_search_tool.search(
                api_call,
                dlc_version=state.dlc_version,
                libraries=state.libraries if state.libraries else None,
            )
            state.api_references.extend(results)

            # Build formatted context for the Agent if available
            if hasattr(self.api_search_tool, 'get_context_for_agent'):
                ctx = self.api_search_tool.get_context_for_agent(
                    api_call,
                    dlc_version=state.dlc_version,
                    libraries=state.libraries if state.libraries else None,
                )
                state.api_context.append(ctx)
        
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
        Stage 3: Generate Lua code using templates, API info, and LLM.

        Uses LLM + RAG context to flesh out templates into real code.
        On regeneration, feeds back validation errors to the LLM.
        Falls back to bare template when LLM is unavailable.
        """
        logger.info("⚙️  Generating Lua code...")
        state.stage = WorkflowStage.GENERATE

        if not state.task:
            state.add_error("Incomplete state for code generation")
            return state

        # Deduplicate and consolidate API context from all searches
        consolidated_context = self._consolidate_api_context(state.api_context)

        # Build feedback from previous validation failures (regeneration loop)
        feedback = ""
        if state.iterations > 1 and state.validation_results:
            failed = [r for r in state.validation_results if not r.is_valid]
            if failed:
                errors_list = []
                for r in failed:
                    errors_list.extend(r.errors)
                if errors_list:
                    feedback = (
                        "\n\nPREVIOUS VALIDATION ERRORS (fix these):\n" +
                        "\n".join(f"- {e}" for e in errors_list)
                    )

        for scaffold_name in state.task.lua_scaffolds:
            template = self.template_manager.get_template(scaffold_name)

            if self.llm:
                try:
                    lua_code = await self._llm_generate(
                        scaffold_type=scaffold_name,
                        template=template,
                        task_title=state.task.title,
                        task_description=state.task.description,
                        api_context=consolidated_context,
                        feedback=feedback,
                        dlc_version=state.dlc_version,
                        libraries=state.libraries,
                    )
                    logger.info(f"🤖 LLM generated code for {scaffold_name} "
                                f"({len(lua_code)} chars)")
                except Exception as e:
                    logger.warning(f"LLM generation failed for {scaffold_name}: {e}, "
                                   f"using template fallback")
                    lua_code = template
            else:
                lua_code = template

            code = GeneratedCode(
                scaffold_type=scaffold_name,
                lua_code=lua_code,
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

    # ------------------------------------------------------------------
    # LLM-based code generation
    # ------------------------------------------------------------------

    async def _llm_generate(
        self,
        scaffold_type: str,
        template: str,
        task_title: str,
        task_description: str,
        api_context: str,
        feedback: str = "",
        dlc_version: str = "REP+",
        libraries: list = None,
    ) -> str:
        """Use LLM to generate Lua code from template + RAG context."""
        if libraries is None:
            libraries = []
        system_prompt = self._build_generation_prompt(
            scaffold_type=scaffold_type,
            template=template,
            task_title=task_title,
            task_description=task_description,
            api_context=api_context,
            dlc_version=dlc_version,
            libraries=libraries,
        )
        if feedback:
            system_prompt += feedback

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Generate the complete Lua mod code for: {task_title}"),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content if hasattr(response, 'content') else str(response)

        return _extract_lua_code(raw)

    @staticmethod
    def _consolidate_api_context(contexts: List[str]) -> str:
        """Deduplicate and merge multiple API context strings into one."""
        seen = set()
        unique = []
        for ctx in contexts:
            if ctx and ctx not in seen:
                seen.add(ctx)
                unique.append(ctx)
        return "\n\n".join(unique)
    
    async def _validate_node(self, state: AgentState) -> AgentState:
        """
        Stage 4: Validate generated Lua code.

        Multi-layered validation:
        1. luacheck (external binary) if available
        2. Python-based Lua syntax check (always runs)
        """
        logger.info("✔️  Validating Lua code...")
        state.stage = WorkflowStage.VALIDATE

        for artifact in state.generated_code:
            code = artifact.lua_code

            # Layer 1: Try luacheck if available
            luacheck_result = _run_luacheck(code)

            # Layer 2: Always run Python-based syntax check
            syntax_errors = _validate_lua_syntax(code)

            if luacheck_result:
                # Merge luacheck findings with basic syntax errors
                all_errors = list(set(luacheck_result.errors + syntax_errors))
                is_valid = luacheck_result.is_valid and not syntax_errors
                result = ValidationResult(
                    is_valid=is_valid,
                    errors=all_errors,
                    warnings=luacheck_result.warnings,
                    luacheck_output=luacheck_result.luacheck_output,
                )
            else:
                # No luacheck — rely on syntax check only
                is_valid = len(syntax_errors) == 0
                result = ValidationResult(
                    is_valid=is_valid,
                    errors=syntax_errors,
                    warnings=[],
                    luacheck_output="" if is_valid else "\n".join(syntax_errors),
                )

            state.validation_results.append(result)

            if not result.is_valid:
                logger.warning(f"⚠️  {artifact.scaffold_type}: {len(result.errors)} error(s)")

        state.add_message(
            "agent",
            f"✅ Validated {len(state.validation_results)} artifacts"
        )
        state.iterations += 1

        valid_count = sum(1 for r in state.validation_results if r.is_valid)
        logger.info(f"✅ Validation: {valid_count}/{len(state.validation_results)} valid")
        return state

    def _validation_router(self, state: AgentState) -> str:
        """Route based on validation results and iteration count."""
        if state.stage == WorkflowStage.ERROR:
            return "error"

        if all(r.is_valid for r in state.validation_results):
            return "complete"

        if state.iterations < self.max_iterations:
            logger.info(f"🔄 Regenerating (iteration {state.iterations}/{self.max_iterations})")
            return "regenerate"

        # Max iterations reached — proceed anyway
        logger.warning(f"⚠️  Max iterations ({self.max_iterations}) reached, proceeding with errors")
        return "complete"
    
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
    
    async def run(
        self,
        user_input: str,
        api_key: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        dlc_version: str = "REP+",
        libraries: Optional[List[str]] = None,
    ) -> AgentState:
        """
        Execute the complete workflow.

        Args:
            user_input: Natural language request from user.
            api_key: User-provided API key (takes priority over env/config).
            provider: LLM provider override (openai/glm/deepseek).
            model: Model name override.
            dlc_version: Target DLC version filter ("REP" or "REP+").
            libraries: List of modding libraries to use (e.g. ["Curlib", "RGON"]).

        Returns:
            Final AgentState with generated artifacts.
        """
        if libraries is None:
            libraries = []
        # If user supplied their own API key, create a fresh LLM for this run
        if api_key and provider:
            from isaac_agent.llm_factory import init_llm
            llm = init_llm(provider=provider, model=model, api_key=api_key)
            if llm:
                self.llm = llm
                logger.info(f"Using user-provided {provider} LLM")
            else:
                logger.warning(f"Failed to init {provider} with user key, falling back")

        session_id = str(uuid.uuid4())[:8]
        logger.info(f"Starting new workflow session: {session_id}")

        # Initialize state
        initial_state = AgentState(
            session_id=session_id,
            user_input=user_input,
            dlc_version=dlc_version,
            libraries=libraries,
        )

        # Execute the compiled graph
        final_state = await self.compiled_graph.ainvoke(initial_state)

        # ainvoke returns a dict — convert back to AgentState for the caller
        if isinstance(final_state, dict):
            state = AgentState(**{k: v for k, v in final_state.items() if k in AgentState.__dataclass_fields__})
            logger.info(f"Workflow {session_id} completed with state: {state.stage.value}")
            return state

        logger.info(f"Workflow {session_id} completed with state: {final_state.stage}")
        return final_state

    def analyze_log_errors(self, source_code: str = "", mod_name: str = "isaac_mod") -> dict:
        """Analyze the Isaac log file for Lua errors and suggest fixes.

        Args:
            source_code: The current Lua source code to attempt fixes on.
            mod_name: Name of the mod for debug output context.

        Returns:
            Dict with errors, fixable flag, fixed_code, debug_code, summary.
        """
        if not self.log_file or not self.log_file.exists():
            return {
                "errors": [],
                "fixable": False,
                "fixed_code": None,
                "debug_code": None,
                "summary": "Log file not found. Run the game first to generate a log.",
            }
        return analyze_and_suggest(str(self.log_file), source_code, mod_name)
    
    def get_workflow_info(self) -> dict:
        """Return information about the workflow"""
        return {
            "name": "Isaac AI Agent",
            "version": "0.1.0",
            "stages": [stage.value for stage in WorkflowStage],
            "max_iterations": self.max_iterations,
            "has_llm": self.llm is not None,
        }
