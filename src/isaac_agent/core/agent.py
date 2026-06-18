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
    FilePlan,
    ModComponent,
)
from isaac_agent.tools.vector_rag import VectorRAG, IsaacAPISearchTool
from isaac_agent.tools.rag_bridge import RAGBridge
from isaac_agent.templates.lua_skeletons import LuaTemplateManager
from isaac_agent.templates.reference_template import ReferenceTemplate
from isaac_agent.templates.patterns import ModArchitectureGuide, FilePattern
from isaac_agent.core.planner import ModPlanner
from isaac_agent.tools.isaac_path_resolver import find_isaac_mods_dir, find_isaac_log_file
from isaac_agent.tools.isaac_error_analyzer import parse_log_errors, analyze_and_suggest
from isaac_agent.xml.schema_parser import XmlSchemaParser
from isaac_agent.xml.scaffold_mapping import resolve_xml_files
from isaac_agent.xml.xml_generator import XmlGenerator
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
    Main orchestrator for the Isaac AI Agent workflow.

    Architecture-first workflow pipeline:
    1. PARSE: Extract structured task from natural language
    2. PLAN: Design complete multi-file project structure
    3. [Per-file loop]: RETRIEVE -> GENERATE -> VALIDATE
    4. XML_GENERATE: Create XML data files
    5. ASSEMBLE: Return final multi-file artifacts
    """

    def __init__(
        self,
        llm: Optional[BaseLanguageModel] = None,
        api_search_tool: Optional[VectorRAG] = None,
        template_manager: Optional[LuaTemplateManager] = None,
        reference_template: Optional[ReferenceTemplate] = None,
        architecture_guide: Optional[ModArchitectureGuide] = None,
        max_iterations: int = 5,
        use_vector_search: bool = True,
    ):
        """Initialize the agent with optional components."""
        self.llm = llm
        self.max_iterations = max_iterations

        # Architecture-first components (new)
        self.reference_template = reference_template or ReferenceTemplate()
        self.architecture_guide = architecture_guide or ModArchitectureGuide()
        self.planner = ModPlanner(
            reference_template=self.reference_template,
            architecture_guide=self.architecture_guide,
            llm=self.llm,
        )

        # Legacy template manager (kept for backward compat, deprecated)
        self.template_manager = template_manager or LuaTemplateManager()

        # Initialize XML schema parser and generator
        cache_path = settings.xml_schema_cache_path if hasattr(settings, 'xml_schema_cache_path') else None
        schema_parser = XmlSchemaParser(cache_path=cache_path)
        self.xml_schemas = schema_parser.parse_all()
        self.xml_generator = XmlGenerator(schemas=self.xml_schemas, llm=self.llm)

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

        logger.info("Isaac AI Agent initialized (architecture-first mode)")

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
        lib_note = ""
        if libraries:
            lib_note = f"\nThe user has selected these modding libraries as dependencies: {', '.join(libraries)}. Prefer API calls that are compatible with these libraries."
        return f"""You are an expert in The Binding of Isaac: Repentance Lua modding.
Your job is to parse a user's mod request into a structured task definition.

Target DLC version: {dlc_version}. Only suggest API functions that are compatible with this version.{lib_note}

Given the user's natural language description, determine:
1. A concise title and detailed description of the mod
2. Which Isaac API functions are needed (use exact names like RegisterMod, GetPlayer, AddHearts, AddCallback, EntitySpawn, Isaac.GetItemIdByName, HasCollectible, etc.)
3. Which mod component types are involved: passive_item, active_item, familiar, room_modifier, player_modifier, custom_entity

Respond with ONLY a JSON object (no markdown, no explanation):
{{
    "title": "<short descriptive title>",
    "description": "<detailed description of what the mod does>",
    "api_calls": ["Function1", "Function2", ...],
    "component_types": ["passive_item", ...]
}}

Choose api_calls using your knowledge of the Isaac modding API."""

    def _build_generation_prompt(
        self,
        file_plan: FilePlan,
        pattern: Optional[FilePattern],
        task_title: str,
        task_description: str,
        api_context: str,
        shared_context: str = "",
        dlc_version: str = "REP+",
        libraries: list = None,
    ) -> str:
        """Build the system prompt for per-file Lua code generation.

        Each file gets a focused prompt with only the context it needs:
        - The file's specific role in the mod architecture
        - Architectural pattern guidance (not a rigid template)
        - Only the APIs this specific file needs
        - Shared Mod_Data context for cross-file consistency
        - Reference example as few-shot pattern
        """
        if libraries is None:
            libraries = []
        lib_note = ""
        if libraries:
            lib_note = f"\nRequired modding libraries: {', '.join(libraries)}. Use their APIs where appropriate."

        pattern_section = ""
        if pattern:
            pattern_section = f"""
Architectural pattern: {pattern.pattern_id}
File role: {pattern.role_description}
Position in include chain: {pattern.include_chain_position}
Callback conventions: {', '.join(pattern.callback_patterns) if pattern.callback_patterns else 'None (base/structural file)'}

Reference example:
```lua
{pattern.reference_code}
```
"""
        shared_section = ""
        if shared_context:
            shared_section = f"""
=== SHARED MOD CONTEXT ===
The following Mod_Data structure is shared across all files in this mod.
Reference these IDs when checking for items in callback functions:

```lua
{shared_context}
```
"""

        # Build naming instruction — inject the concrete example when this is an item file
        naming_rule = ""
        if file_plan.relative_path.startswith("scripts/items/") and not file_plan.relative_path.endswith("!items.lua"):
            naming_rule = """
=== NAMING RULES FOR THIS FILE ===
The names Item1/Item2/passive_function1 in the reference pattern are FORMAT PLACEHOLDERS.
You MUST replace them with descriptive names derived from the user's request.

Example (user asks for "翻倍伤害的被动道具"):
  item1 -> damage_multiplier (lowercase_with_underscores for file names)
  Item1 -> DamageMultiplier (PascalCase for Mod_Data keys)
  passive_function1 -> damage_multiplier_effect (descriptive function name)
  "item1" -> "damage_multiplier" (string passed to Isaac.GetItemIdByName)

Your function names MUST reflect what the item DOES. Be creative.
Read the mod task description and derive real English names from it.
"""

        return f"""You are an expert Lua modder for The Binding of Isaac: Repentance.
Generate complete, working Lua code for a SPECIFIC FILE in a multi-file mod project.

Target DLC version: {dlc_version}. Only use APIs compatible with {dlc_version}.{lib_note}

=== MOD TASK ===
Title: {task_title}
Description: {task_description}

=== THIS FILE ===
Path: {file_plan.relative_path}
Role: {file_plan.role_description}
{pattern_section}
{shared_section}
{naming_rule}
=== API DOCUMENTATION FOR THIS FILE ===
{api_context if api_context else "Use standard Isaac modding API patterns (RegisterMod, AddCallback, etc.)"}

Instructions:
1. Generate ONLY the code for this specific file ({file_plan.relative_path})
2. This is ONE file in a multi-file mod — do NOT include RegisterMod or includes unless this IS main.lua
3. For item scripts: reference Mod_Data.Info.Items.{ItemName} for item IDs (defined in scripts/data/data.lua)
4. Handle edge cases and errors appropriately
5. Return ONLY the complete Lua code (or XML for xml files), no markdown fences, no explanations
6. The code must be syntactically valid Lua
7. Do NOT generate code for other files — focus ONLY on {file_plan.relative_path}
8. CRITICAL: Replace ALL placeholder names from the reference pattern with descriptive English names derived from the user's task. Use ASCII-only, descriptive identifiers that reflect what the item DOES."""

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
            lua_scaffolds=parsed.get("component_types", parsed.get("lua_scaffolds", [])),
            dlc_version=dlc_version,
            libraries=libraries,
        )

        # Validate component types against known components
        valid_components = [
            c for c in task.lua_scaffolds
            if c in ("passive_item", "active_item", "familiar", "room_modifier", "player_modifier", "custom_entity")
        ]
        if valid_components:
            task.lua_scaffolds = valid_components
        else:
            task.lua_scaffolds = ["passive_item"]

        return task

    def _fallback_parse(self, user_input: str) -> TaskDefinition:
        """Keyword-based fallback parser when LLM is unavailable."""
        user_lower = user_input.lower()

        # Map keywords to likely API calls
        api_keywords = {
            "health": ["GetPlayer", "AddHearts"],
            "heart": ["GetPlayer", "AddHearts", "AddSoulHearts"],
            "player": ["GetPlayer"],
            "item": ["Isaac.GetItemIdByName", "HasCollectible"],
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
            "passive": ["HasCollectible", "MC_POST_EVALUATE_CACHE", "Game.GetNumPlayers"],
            "active": ["MC_USE_ITEM", "HasCollectible"],
            "familiar": ["MC_FAMILIAR_INIT", "MC_FAMILIAR_UPDATE"],
            "跟班": ["MC_FAMILIAR_INIT", "MC_FAMILIAR_UPDATE"],
            "主动": ["MC_USE_ITEM", "HasCollectible"],
            "被动": ["HasCollectible", "MC_POST_EVALUATE_CACHE"],
        }
        api_calls = set()
        api_calls.add("RegisterMod")
        for keyword, funcs in api_keywords.items():
            if keyword in user_lower:
                api_calls.update(funcs)

        # Map keywords to component types (new architecture-first system)
        component_keywords = {
            "passive_item": ["被动", "passive", "被动道具", "属性", "stat", "cache", "item"],
            "active_item": ["主动", "active", "主动道具", "使用", "use item", "charge", "充能"],
            "familiar": ["跟班", "familiar", "宠物", "companion", "follow"],
            "room_modifier": ["房间", "room", "层", "floor", "stage"],
            "player_modifier": ["player", "玩家", "角色", "character", "初始"],
            "custom_entity": ["entity", "enemy", "敌人", "实体", "boss"],
        }
        components = set()
        for comp_type, keywords in component_keywords.items():
            if any(kw in user_lower for kw in keywords):
                components.add(comp_type)

        if not components:
            components.add("passive_item")

        return TaskDefinition(
            original_request=user_input,
            title=user_input[:60],
            description=user_input,
            api_calls=list(api_calls),
            lua_scaffolds=list(components),
        )
    
    def _build_graph(self) -> StateGraph:
        """Construct the LangGraph workflow — architecture-first pipeline."""
        workflow = StateGraph(AgentState)

        # Add nodes for each workflow stage
        workflow.add_node("parse", self._parse_node)
        workflow.add_node("plan", self._plan_node)
        workflow.add_node("retrieve", self._retrieve_file_node)
        workflow.add_node("generate", self._generate_file_node)
        workflow.add_node("validate", self._validate_node)
        workflow.add_node("xml_generate", self._xml_generate_node)
        workflow.add_node("assemble", self._assemble_node)
        workflow.add_node("error_handler", self._error_handler_node)

        # Define edges: parse -> plan -> retrieve -> generate -> validate
        workflow.add_edge("parse", "plan")
        workflow.add_edge("plan", "retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", "validate")

        # Conditional edge from validate: 4-way route
        workflow.add_conditional_edges(
            "validate",
            self._validation_router,
            {
                "next_file": "retrieve",
                "xml_generate": "xml_generate",
                "regenerate": "generate",
                "error": "error_handler",
            }
        )

        workflow.add_edge("xml_generate", "assemble")
        workflow.add_edge("assemble", END)
        workflow.add_edge("error_handler", END)

        # Set entry point
        workflow.set_entry_point("parse")

        return workflow

    # ------------------------------------------------------------------
    # NODE: Parse
    # ------------------------------------------------------------------

    async def _parse_node(self, state: AgentState) -> AgentState:
        """Stage 1: Parse natural language input into structured task."""
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
                            f"api_calls={task.api_calls}, components={task.lua_scaffolds}")
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

    # ------------------------------------------------------------------
    # NODE: Plan (NEW — architecture-first)
    # ------------------------------------------------------------------

    async def _plan_node(self, state: AgentState) -> AgentState:
        """Stage 2: Design the complete multi-file project architecture.

        Uses ModPlanner to classify the mod type and design the file tree
        BEFORE any code is generated.
        """
        logger.info("🏗️  Planning mod architecture...")
        state.stage = WorkflowStage.PLAN

        if not state.task:
            state.add_error("No task available for planning")
            return state

        plans, shared_context = await self.planner.design_architecture(
            task=state.task,
            dlc_version=state.dlc_version,
            libraries=state.libraries,
        )

        state.file_plans = plans
        state.shared_context = shared_context
        state.current_file_index = 0
        state.file_iterations = 0

        # Log the planned file tree
        tree_lines = ["\n📁 Planned mod structure:"]
        for fp in plans:
            icon = "📄" if fp.is_xml else "📜"
            tree_lines.append(f"  {icon} {fp.relative_path} — {fp.role_description}")
        logger.info("\n".join(tree_lines))

        state.add_message(
            "agent",
            f"🏗️ Designed architecture: {len(plans)} files across {len([p for p in plans if not p.is_xml])} Lua + {len([p for p in plans if p.is_xml])} XML",
        )
        state.iterations += 1

        return state

    # ------------------------------------------------------------------
    # NODE: Retrieve File (per-file API retrieval)
    # ------------------------------------------------------------------

    async def _retrieve_file_node(self, state: AgentState) -> AgentState:
        """Retrieve APIs for the CURRENT file only (focused context)."""
        if state.current_file_index >= len(state.file_plans):
            state.all_files_generated = True
            return state

        current_plan = state.file_plans[state.current_file_index]
        logger.info(f"🔍 [{state.current_file_index + 1}/{len(state.file_plans)}] Retrieving APIs for: {current_plan.relative_path}")

        state.stage = WorkflowStage.RETRIEVE_FILE

        # Clear previous file's API context
        state.api_context = []

        # Skip XML files — they go through the dedicated XML generator
        if current_plan.is_xml:
            logger.info(f"  Skipping API retrieval for XML file: {current_plan.relative_path}")
            return state

        # Search for APIs this specific file needs
        all_apis = list(current_plan.required_apis)
        if state.task:
            all_apis.extend(state.task.api_calls)

        searched = set()
        for api_call in all_apis:
            if api_call in searched:
                continue
            searched.add(api_call)

            try:
                results = self.api_search_tool.search(
                    api_call,
                    dlc_version=state.dlc_version,
                    libraries=state.libraries if state.libraries else None,
                )
                state.api_references.extend(results)

                if hasattr(self.api_search_tool, 'get_context_for_agent'):
                    ctx = self.api_search_tool.get_context_for_agent(
                        api_call,
                        dlc_version=state.dlc_version,
                        libraries=state.libraries if state.libraries else None,
                    )
                    if ctx:
                        state.api_context.append(ctx)
            except Exception as e:
                logger.warning(f"  API search failed for '{api_call}': {e}")

        logger.info(f"  Retrieved {len(state.api_context)} API contexts for {current_plan.relative_path}")
        return state

    # ------------------------------------------------------------------
    # NODE: Generate File (per-file code generation)
    # ------------------------------------------------------------------

    async def _generate_file_node(self, state: AgentState) -> AgentState:
        """Generate code for the CURRENT file only.

        Each file gets:
        - Its specific FilePlan (role, path)
        - Its architectural pattern (conventions, reference code)
        - Only the APIs it needs (focused, not a full dump)
        - Shared Mod_Data context for cross-file consistency
        - Validation feedback from previous attempts on THIS file
        """
        if state.current_file_index >= len(state.file_plans):
            state.all_files_generated = True
            return state

        current_plan = state.file_plans[state.current_file_index]
        logger.info(f"⚙️  [{state.current_file_index + 1}/{len(state.file_plans)}] Generating: {current_plan.relative_path}")

        state.stage = WorkflowStage.GENERATE_FILE
        state.file_iterations += 1

        if not state.task:
            state.add_error("No task for code generation")
            return state

        # On regeneration: pop the failed artifact so it gets replaced
        if state.file_iterations > 1 and state.generated_code:
            popped = state.generated_code.pop()
            logger.info(f"  🔄 Replacing failed artifact: {popped.file_path or popped.scaffold_type}")

        # Get the architectural pattern for this file
        pattern = self.architecture_guide.get_pattern(current_plan.template_hint)

        # Consolidate API context for this file
        consolidated_context = self._consolidate_api_context(state.api_context)

        # Build feedback from validation failures on this file (regeneration)
        feedback = ""
        if state.file_iterations > 1 and state.validation_results:
            last_result = state.validation_results[-1] if state.validation_results else None
            if last_result and not last_result.is_valid:
                errors_list = last_result.errors
                if errors_list:
                    feedback = (
                        "\n\nPREVIOUS VALIDATION ERRORS (fix these in this file):\n" +
                        "\n".join(f"- {e}" for e in errors_list)
                    )

        # Generate the code (XML files handled separately)
        if current_plan.is_xml:
            lua_code = ""  # XML files handled in _xml_generate_node
        elif self.llm:
            try:
                lua_code = await self._llm_generate_file(
                    file_plan=current_plan,
                    pattern=pattern,
                    task_title=state.task.title,
                    task_description=state.task.description,
                    api_context=consolidated_context,
                    shared_context=state.shared_context,
                    feedback=feedback,
                    dlc_version=state.dlc_version,
                    libraries=state.libraries,
                )
                logger.info(f"  LLM generated {len(lua_code)} chars")
            except Exception as e:
                logger.warning(f"  LLM generation failed for {current_plan.relative_path}: {e}")
                lua_code = self._get_fallback_code(current_plan, pattern)
        else:
            lua_code = self._get_fallback_code(current_plan, pattern)

        code = GeneratedCode(
            scaffold_type=current_plan.template_hint,
            lua_code=lua_code,
            file_path=current_plan.relative_path,
            role_description=current_plan.role_description,
            requires_validation=not current_plan.is_xml,
        )
        state.generated_code.append(code)

        state.add_message(
            "agent",
            f"✨ Generated {current_plan.relative_path} ({len(lua_code)} chars)"
        )

        logger.info(f"  Generated: {current_plan.relative_path}")
        return state

    def _get_fallback_code(self, file_plan: FilePlan, pattern: Optional[FilePattern]) -> str:
        """Get fallback code when LLM is unavailable."""
        if pattern and pattern.reference_code:
            return pattern.reference_code
        return f"-- {file_plan.relative_path}\n-- Role: {file_plan.role_description}\n-- TODO: Implement\n"

    # ------------------------------------------------------------------
    # Per-file LLM code generation
    # ------------------------------------------------------------------

    async def _llm_generate_file(
        self,
        file_plan: FilePlan,
        pattern: Optional[FilePattern],
        task_title: str,
        task_description: str,
        api_context: str,
        shared_context: str = "",
        feedback: str = "",
        dlc_version: str = "REP+",
        libraries: list = None,
    ) -> str:
        """Use LLM to generate code for a single file with focused context."""
        if libraries is None:
            libraries = []
        system_prompt = self._build_generation_prompt(
            file_plan=file_plan,
            pattern=pattern,
            task_title=task_title,
            task_description=task_description,
            api_context=api_context,
            shared_context=shared_context,
            dlc_version=dlc_version,
            libraries=libraries,
        )
        if feedback:
            system_prompt += feedback

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Generate code for: {file_plan.relative_path} — {file_plan.role_description}"),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content if hasattr(response, 'content') else str(response)

        # For XML files, return the raw content (will be processed by XML generator)
        if file_plan.is_xml or file_plan.relative_path.endswith(".xml"):
            return _extract_lua_code(raw)  # same extraction logic works for XML in markdown

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

    async def _xml_generate_node(self, state: AgentState) -> AgentState:
        """
        Stage 3.5: Generate XML data files based on generated Lua code.

        Uses LLM with XML schema context when available;
        falls back to programmatic generation.
        """
        logger.info("📄 Generating XML files...")
        state.stage = WorkflowStage.XML_GENERATE

        if not state.task:
            state.add_error("No task for XML generation")
            return state

        state.generated_xml = []

        # Shared ID context so entries across files get unique IDs
        from isaac_agent.xml.xml_generator import XmlGenerationContext
        safe_title = "".join(c if c.isalnum() else "_" for c in state.task.title).strip("_").lower()
        shared_ctx = XmlGenerationContext(mod_name=safe_title, task_title=state.task.title)
        self.xml_generator._shared_context = shared_ctx

        for i, code in enumerate(state.generated_code):
            scaffold = code.scaffold_type
            xml_files = resolve_xml_files(
                scaffolds=[scaffold],
                task_description=state.task.description,
                lua_code=code.lua_code,
            )

            for xml_spec in xml_files:
                result = self.xml_generator.generate(
                    xml_file=xml_spec["xml_file"],
                    task_title=state.task.title,
                    task_description=state.task.description,
                    lua_code=code.lua_code,
                    scaffold_type=scaffold,
                    dlc_version=state.dlc_version,
                )
                if result and result.entries:
                    state.generated_xml.append(result)
                    logger.info(f"  Generated {xml_spec['xml_file']}: "
                                f"{len(result.entries)} entry(s) [{result.generated_by}]")

        # Merge entries that target the same XML file
        state.generated_xml = self._merge_xml_entries(state.generated_xml)

        xml_summary = ", ".join(
            f"{g.xml_file}({len(g.entries)})"
            for g in state.generated_xml
        ) if state.generated_xml else "none"

        state.add_message(
            "agent",
            f"📄 Generated XML files: {xml_summary}",
        )

        logger.info(f"✅ Generated {len(state.generated_xml)} XML files")
        return state

    @staticmethod
    def _merge_xml_entries(generated: List[Any]) -> List[Any]:
        """Merge GeneratedXml objects that target the same XML file."""
        from isaac_agent.xml.xml_generator import XmlGenerator
        return XmlGenerator.merge_xml_files(generated)

    async def _validate_node(self, state: AgentState) -> AgentState:
        """Validate the CURRENT file's generated code.

        On next_file / regenerate routes, validates only the latest artifact.
        """
        logger.info("✔️  Validating current file...")
        state.stage = WorkflowStage.VALIDATE

        # Only validate the latest (current file's) artifact
        if not state.generated_code:
            state.validation_results.append(ValidationResult(is_valid=True))
            return state

        artifact = state.generated_code[-1]

        # For XML files and empty/fallback code, skip actual validation
        # but still advance the file index (this is critical for the per-file loop)
        current_plan = None
        if state.current_file_index < len(state.file_plans):
            current_plan = state.file_plans[state.current_file_index]

        if current_plan and current_plan.is_xml:
            state.validation_results.append(ValidationResult(is_valid=True))
            logger.info(f"  Skipped validation for XML: {current_plan.relative_path}")
            state.current_file_index += 1
            state.file_iterations = 0
            return state

        code = artifact.lua_code

        # Skip validation for empty/fallback code
        if not code or code.startswith("-- TODO:"):
            state.validation_results.append(ValidationResult(
                is_valid=True,
                warnings=["Fallback/empty code — no validation performed"],
            ))
            state.current_file_index += 1
            state.file_iterations = 0
            return state

        # Layer 1: Try luacheck if available
        luacheck_result = _run_luacheck(code)

        # Layer 2: Always run Python-based syntax check
        # Skip RegisterMod check for non-main files
        syntax_errors = _validate_lua_syntax(code)
        if artifact.file_path and artifact.file_path != "main.lua":
            syntax_errors = [e for e in syntax_errors if "RegisterMod" not in e]

        if luacheck_result:
            all_errors = list(set(luacheck_result.errors + syntax_errors))
            is_valid = luacheck_result.is_valid and not syntax_errors
            result = ValidationResult(
                is_valid=is_valid,
                errors=all_errors,
                warnings=luacheck_result.warnings,
                luacheck_output=luacheck_result.luacheck_output,
            )
        else:
            is_valid = len(syntax_errors) == 0
            result = ValidationResult(
                is_valid=is_valid,
                errors=syntax_errors,
                warnings=[],
                luacheck_output="" if is_valid else "\n".join(syntax_errors),
            )

        state.validation_results.append(result)

        if not result.is_valid:
            logger.warning(f"  ⚠️  {artifact.file_path or artifact.scaffold_type}: {len(result.errors)} error(s)")
            # If max per-file retries exceeded, skip this file and advance
            if state.file_iterations >= self.max_iterations:
                logger.warning(f"  ⏭️  Skipping file after {state.file_iterations} failed attempts")
                state.current_file_index += 1
                state.file_iterations = 0
        else:
            logger.info(f"  ✅ {artifact.file_path or artifact.scaffold_type}: valid")
            # Advance to next file for the next iteration
            state.current_file_index += 1
            state.file_iterations = 0

        state.add_message("agent", f"✔️ Validated {artifact.file_path or artifact.scaffold_type}")
        return state

    def _validation_router(self, state: AgentState) -> str:
        """Route based on validation of the CURRENT file.

        IMPORTANT: This is a LangGraph conditional edge function — it must NOT
        modify state. State modifications happen in the nodes.

        4-way routing:
        - next_file: current file valid, more files remain
        - xml_generate: all files done, proceed to XML generation
        - regenerate: current file failed, retry (if under max iterations)
        - error: unrecoverable error
        """
        if state.stage == WorkflowStage.ERROR:
            return "error"

        if not state.validation_results:
            return "error"

        last_result = state.validation_results[-1]

        if last_result.is_valid:
            # Check if there are more files to process
            if state.current_file_index >= len(state.file_plans):
                logger.info("All files generated and validated, proceeding to XML generation")
                state.all_files_generated = True
                return "xml_generate"
            logger.info(f"➡️  Proceeding to file {state.current_file_index + 1}/{len(state.file_plans)}")
            return "next_file"

        # Current file failed validation — can we retry?
        if state.file_iterations < self.max_iterations:
            logger.info(f"🔄 Regenerating current file (attempt {state.file_iterations}/{self.max_iterations})")
            return "regenerate"

        # Max per-file retries reached — skip this file and advance
        logger.warning(f"⚠️  Max retries ({self.max_iterations}) for current file, skipping")
        # Force advance in node since router can't modify state
        return "next_file"

    # ------------------------------------------------------------------
    # NODE: Assemble (final stage)
    # ------------------------------------------------------------------

    async def _assemble_node(self, state: AgentState) -> AgentState:
        """Final stage: Mark workflow as complete with multi-file artifacts."""
        logger.info("🎉 Workflow complete — multi-file mod assembled!")
        state.stage = WorkflowStage.COMPLETE
        state.add_message(
            "agent",
            f"✅ Generated {len(state.generated_code)} files across {len(state.file_plans)} planned paths",
        )
        return state

    async def _error_handler_node(self, state: AgentState) -> AgentState:
        """Handle workflow errors."""
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
