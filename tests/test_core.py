"""
Basic tests for Isaac AI Agent
"""

import pytest
import asyncio
from isaac_agent.core.agent import MainAgent
from isaac_agent.core.state import (
    AgentState, 
    WorkflowStage,
    TaskDefinition,
    APIReference,
)
from isaac_agent.tools.vector_rag import VectorRAG, IsaacAPIDatabase
from isaac_agent.templates.lua_skeletons import LuaTemplateManager


class TestAgent:
    """Test Agent initialization and workflow"""

    def test_agent_initialization(self):
        """Test that agent initializes correctly"""
        agent = MainAgent()
        assert agent is not None
        assert agent.api_search_tool is not None
        assert agent.template_manager is not None

    def test_agent_info(self):
        """Test agent info method"""
        agent = MainAgent()
        info = agent.get_workflow_info()
        assert info["name"] == "Isaac AI Agent"
        assert "stages" in info

    def test_fallback_parse_health(self):
        agent = MainAgent()
        task = agent._fallback_parse("add health to the player on room clear")
        assert "RegisterMod" in task.api_calls
        assert len(task.lua_scaffolds) > 0
        assert len(task.api_calls) > 1  # Should detect health + room

    def test_fallback_parse_item(self):
        agent = MainAgent()
        task = agent._fallback_parse("create a custom item that gives coins")
        assert "RegisterMod" in task.api_calls
        assert "passive_item" in task.lua_scaffolds or "active_item" in task.lua_scaffolds
        assert "AddCoins" in task.api_calls or "Isaac.GetItemIdByName" in task.api_calls

    def test_fallback_parse_entity(self):
        agent = MainAgent()
        task = agent._fallback_parse("spawn a custom enemy that explodes on death")
        assert "custom_entity" in task.lua_scaffolds
        assert "EntitySpawn" in task.api_calls or "SpawnExplosion" in task.api_calls

    def test_fallback_parse_unknown(self):
        agent = MainAgent()
        task = agent._fallback_parse("xyzzy foobar nothing")
        assert "RegisterMod" in task.api_calls
        assert len(task.lua_scaffolds) == 1
        assert task.lua_scaffolds[0] == "passive_item"

    def test_extract_json_direct(self):
        from isaac_agent.core.agent import _extract_json
        result = _extract_json('{"a": 1, "b": [2, 3]}')
        assert result == {"a": 1, "b": [2, 3]}

    def test_extract_json_markdown_block(self):
        from isaac_agent.core.agent import _extract_json
        # Use chr(96) to avoid shell escaping issues
        bt = chr(96) * 3
        result = _extract_json(f'{bt}json\n{{"x": "y"}}\n{bt}')
        assert result == {"x": "y"}

    def test_extract_json_embedded(self):
        from isaac_agent.core.agent import _extract_json
        result = _extract_json('some text {"c": 3} more text')
        assert result == {"c": 3}

    def test_extract_json_invalid(self):
        from isaac_agent.core.agent import _extract_json
        import pytest
        with pytest.raises(ValueError):
            _extract_json("no json anywhere in this string")

    def test_extract_lua_code_plain(self):
        from isaac_agent.core.agent import _extract_lua_code
        code = "local x = 1\nreturn x"
        assert _extract_lua_code(code) == code

    def test_extract_lua_code_fenced(self):
        from isaac_agent.core.agent import _extract_lua_code
        bt = chr(96) * 3
        code = f"{bt}lua\nlocal mod = RegisterMod('Test', 1)\n{bt}"
        result = _extract_lua_code(code)
        assert result == "local mod = RegisterMod('Test', 1)"

    def test_extract_lua_code_no_lang(self):
        from isaac_agent.core.agent import _extract_lua_code
        bt = chr(96) * 3
        code = f"{bt}\nlocal x = 1\n{bt}"
        result = _extract_lua_code(code)
        assert result == "local x = 1"

    def test_consolidate_api_context(self):
        from isaac_agent.core.agent import MainAgent
        ctxs = ["[API Context]\nFunction: A\n---", "duplicate", "duplicate"]
        result = MainAgent._consolidate_api_context(ctxs)
        assert "Function: A" in result
        assert result.count("duplicate") == 1  # deduplicated

    def test_consolidate_api_context_empty(self):
        from isaac_agent.core.agent import MainAgent
        assert MainAgent._consolidate_api_context([]) == ""
        assert MainAgent._consolidate_api_context(["", ""]) == ""


class TestVectorRAG:
    """Test advanced RAG with vector search"""

    @pytest.fixture(autouse=True)
    def _setup(self, tmp_path):
        """Use isolated index path to avoid pollution from KB tests."""
        self._index_dir = tmp_path / "core_test"
        self._index_dir.mkdir()
        self._index_path = str(self._index_dir / "test.faiss")

    def test_tool_initialization(self):
        """Test tool initializes"""
        tool = VectorRAG(embedding_model="huggingface", faiss_index_path=self._index_path)
        assert tool is not None

    def test_search_by_query(self):
        """Test semantic search"""
        tool = VectorRAG(embedding_model="huggingface", faiss_index_path=self._index_path)
        results = tool.search("player health modification", top_k=3)
        assert len(results) > 0
        assert "function_name" in results[0]

    def test_get_function_info(self):
        """Test getting specific function info"""
        tool = VectorRAG(embedding_model="huggingface", faiss_index_path=self._index_path)
        info = tool.get_function_info("GetPlayer")
        assert info is not None
        assert info["category"] == "Player Access"

    def test_list_categories(self):
        """Test listing categories"""
        tool = VectorRAG(embedding_model="huggingface", faiss_index_path=self._index_path)
        categories = tool.list_categories()
        assert len(categories) > 0
        assert "Player Access" in categories

    def test_api_database(self):
        """Test API database"""
        db = IsaacAPIDatabase.DATABASE
        assert "GetPlayer" in db
        assert len(db) >= 20

    def test_fallback_search(self):
        """Test fallback keyword search"""
        tool = VectorRAG(embedding_model=None, faiss_index_path=self._index_path)
        results = tool._fallback_search("item")
        assert len(results) > 0


class TestLuaTemplateManager:
    """Test Lua template management"""
    
    def test_manager_initialization(self):
        """Test manager initializes"""
        manager = LuaTemplateManager()
        assert manager is not None
    
    def test_get_template(self):
        """Test getting a template"""
        manager = LuaTemplateManager()
        template = manager.get_template("MOD_INIT")
        assert template is not None
        assert "RegisterMod" in template
    
    def test_list_templates(self):
        """Test listing templates"""
        manager = LuaTemplateManager()
        templates = manager.list_templates()
        assert len(templates) > 0
        assert "MOD_INIT" in templates
    
    def test_find_templates(self):
        """Test finding templates by query"""
        manager = LuaTemplateManager()
        matches = manager.find_templates("item")
        assert len(matches) > 0
    
    def test_validate_template(self):
        """Test template validation"""
        manager = LuaTemplateManager()
        assert manager.validate_template("MOD_INIT") is True
        assert manager.validate_template("NONEXISTENT") is False


class TestAgentState:
    """Test Agent state management"""
    
    def test_state_initialization(self):
        """Test state initializes correctly"""
        state = AgentState(session_id="test-123")
        assert state.session_id == "test-123"
        assert state.stage == WorkflowStage.PARSE
        assert len(state.messages) == 0
    
    def test_add_message(self):
        """Test adding messages"""
        state = AgentState(session_id="test-123")
        state.add_message("agent", "Test message")
        assert len(state.messages) == 1
        assert state.messages[0]["role"] == "agent"
    
    def test_add_error(self):
        """Test adding errors"""
        state = AgentState(session_id="test-123")
        state.add_error("Test error")
        assert len(state.errors) == 1
        assert state.stage == WorkflowStage.ERROR
    
    def test_state_to_dict(self):
        """Test state serialization"""
        state = AgentState(session_id="test-123", user_input="Test input")
        state_dict = state.to_dict()
        assert state_dict["session_id"] == "test-123"
        assert state_dict["user_input"] == "Test input"


@pytest.mark.asyncio
class TestWorkflow:
    """Test complete workflow execution"""
    
    async def test_workflow_execution(self):
        """Test running a complete workflow"""
        agent = MainAgent()
        result = await agent.run("Create a simple mod")

        assert result is not None
        # ainvoke can return dict or AgentState
        if isinstance(result, dict):
            session_id = result.get("session_id")
            stage = result.get("stage")
        else:
            session_id = result.session_id
            stage = result.stage
        assert session_id is not None
        assert stage is not None


class TestReferenceTemplate:
    """Test the gold-standard reference template module."""

    def test_template_has_nine_files(self):
        from isaac_agent.templates.reference_template import ReferenceTemplate
        rt = ReferenceTemplate()
        assert len(rt.FILES) == 9

    def test_always_required_files(self):
        from isaac_agent.templates.reference_template import ReferenceTemplate
        rt = ReferenceTemplate()
        required = rt.get_always_required_files()
        required_paths = {f.relative_path for f in required}
        assert "main.lua" in required_paths
        assert "metadata.xml" in required_paths
        assert "scripts/common.lua" in required_paths
        assert "scripts/data/data.lua" in required_paths

    def test_get_files_for_component(self):
        from isaac_agent.templates.reference_template import ReferenceTemplate
        rt = ReferenceTemplate()
        files = rt.get_files_for_component("passive_item")
        paths = {f.relative_path for f in files}
        assert "scripts/items/item1.lua" in paths
        assert "content/items.xml" in paths

    def test_include_chain_order(self):
        from isaac_agent.templates.reference_template import ReferenceTemplate
        rt = ReferenceTemplate()
        chain = rt.get_include_chain()
        assert chain[0] == "main.lua"
        assert chain[-1] == "scripts/items/item3.lua"

    def test_prompt_context(self):
        from isaac_agent.templates.reference_template import ReferenceTemplate
        rt = ReferenceTemplate()
        ctx = rt.as_prompt_context()
        assert "GOLD-STANDARD" in ctx
        assert "main.lua" in ctx
        assert "Include chain" in ctx


class TestModArchitectureGuide:
    """Test the architectural patterns module."""

    def test_all_patterns_present(self):
        from isaac_agent.templates.patterns import ModArchitectureGuide
        ag = ModArchitectureGuide()
        patterns = ag.list_patterns()
        assert "main_lua" in patterns
        assert "passive_item_script" in patterns
        assert "active_item_script" in patterns
        assert "familiar_script" in patterns
        assert "data_lua" in patterns

    def test_get_pattern(self):
        from isaac_agent.templates.patterns import ModArchitectureGuide
        ag = ModArchitectureGuide()
        p = ag.get_pattern("main_lua")
        assert p is not None
        assert p.relative_path_template == "main.lua"
        assert p.is_base_file is True

    def test_get_base_patterns(self):
        from isaac_agent.templates.patterns import ModArchitectureGuide
        ag = ModArchitectureGuide()
        base = ag.get_base_patterns()
        base_ids = {p.pattern_id for p in base}
        assert "main_lua" in base_ids
        assert "common_lua" in base_ids
        assert "data_lua" in base_ids

    def test_get_patterns_for_component(self):
        from isaac_agent.templates.patterns import ModArchitectureGuide
        ag = ModArchitectureGuide()
        patterns = ag.get_patterns_for_component("passive_item")
        ids = {p.pattern_id for p in patterns}
        assert "passive_item_script" in ids
        assert "data_lua" in ids

    def test_prompt_context(self):
        from isaac_agent.templates.patterns import ModArchitectureGuide
        ag = ModArchitectureGuide()
        patterns = [ag.get_pattern("passive_item_script")]
        ctx = ag.as_prompt_context(patterns)
        assert "MC_POST_EVALUATE_CACHE" in ctx


class TestModPlanner:
    """Test the architecture-first planner module."""

    def test_planner_initialization(self):
        from isaac_agent.core.planner import ModPlanner
        from isaac_agent.templates.reference_template import ReferenceTemplate
        from isaac_agent.templates.patterns import ModArchitectureGuide
        planner = ModPlanner(
            reference_template=ReferenceTemplate(),
            architecture_guide=ModArchitectureGuide(),
        )
        assert planner is not None

    def test_classify_passive_item(self):
        from isaac_agent.core.planner import ModPlanner
        from isaac_agent.core.state import TaskDefinition
        planner = ModPlanner()
        task = TaskDefinition(
            original_request="passive item that doubles damage",
            title="Damage Doubler",
            description="A passive item that doubles the player's damage",
            api_calls=["HasCollectible"],
            lua_scaffolds=["passive_item"],
        )
        components = planner.classify_mod_type(task)
        assert len(components) >= 1
        assert any(c.component_type == "passive_item" for c in components)

    def test_fallback_plan_creates_file_tree(self):
        import asyncio
        from isaac_agent.core.planner import ModPlanner
        from isaac_agent.core.state import TaskDefinition
        planner = ModPlanner()
        task = TaskDefinition(
            original_request="make a passive item",
            title="Test Item",
            description="A passive item",
            api_calls=["HasCollectible"],
            lua_scaffolds=["passive_item"],
        )
        plans, shared = asyncio.run(planner.design_architecture(task))
        assert len(plans) >= 5  # main, metadata, common, data, items_init, item, items.xml = 7
        paths = {p.relative_path for p in plans}
        assert "main.lua" in paths
        assert "scripts/data/data.lua" in paths
        assert "metadata.xml" in paths
        assert "content/items.xml" in paths
        # At least one item script
        item_files = [p for p in plans if p.relative_path.startswith("scripts/items/") and not p.is_xml]
        assert len(item_files) >= 2  # !items.lua + item script

    def test_shared_context_generation(self):
        import asyncio
        from isaac_agent.core.planner import ModPlanner
        from isaac_agent.core.state import TaskDefinition
        planner = ModPlanner()
        task = TaskDefinition(
            original_request="damage doubler passive",
            title="Damage Doubler",
            description="Passive item that doubles damage",
            api_calls=["HasCollectible"],
            lua_scaffolds=["passive_item"],
        )
        _, shared = asyncio.run(planner.design_architecture(task))
        assert "Mod_Data" in shared
        assert "Isaac.GetItemIdByName" in shared


class TestFilePlanState:
    """Test the new FilePlan and ModComponent state models."""

    def test_file_plan_creation(self):
        from isaac_agent.core.state import FilePlan
        plan = FilePlan(
            relative_path="scripts/items/test.lua",
            role_description="Test passive item",
            required_apis=["HasCollectible"],
            template_hint="passive_item_script",
        )
        assert plan.relative_path == "scripts/items/test.lua"
        assert plan.is_xml is False
        assert "HasCollectible" in plan.required_apis

    def test_mod_component_creation(self):
        from isaac_agent.core.state import ModComponent
        comp = ModComponent(
            component_type="passive_item",
            name="Test",
            description="A test item",
        )
        assert comp.component_type == "passive_item"

    def test_generated_code_has_new_fields(self):
        from isaac_agent.core.state import GeneratedCode
        code = GeneratedCode(
            scaffold_type="passive_item_script",
            lua_code="local x = 1",
            file_path="scripts/items/test.lua",
            role_description="Passive item script",
        )
        assert code.file_path == "scripts/items/test.lua"
        assert code.role_description == "Passive item script"

    def test_agent_state_has_new_fields(self):
        from isaac_agent.core.state import AgentState
        state = AgentState(session_id="test")
        assert state.file_plans == []
        assert state.current_file_index == 0
        assert state.mod_components == []
        assert state.all_files_generated is False
        assert state.shared_context == ""
        assert state.file_iterations == 0


class TestMultiFileBuild:
    """Test the multi-file build system."""

    def test_build_with_file_paths(self, tmp_path):
        from isaac_agent.build import ModBuilder
        from isaac_agent.core.state import GeneratedCode
        builder = ModBuilder(output_dir=str(tmp_path))
        artifacts = [
            GeneratedCode(
                scaffold_type="main_lua",
                lua_code='local mod = RegisterMod("test", 1)\ninclude("scripts.common")',
                file_path="main.lua",
            ),
            GeneratedCode(
                scaffold_type="common_lua",
                lua_code='include("scripts.data.data")\ninclude("scripts.items.!items")',
                file_path="scripts/common.lua",
            ),
            GeneratedCode(
                scaffold_type="data_lua",
                lua_code='local Mod_Data = {Info = {Items = {}}}',
                file_path="scripts/data/data.lua",
            ),
        ]
        mod_dir = builder.build(
            artifacts=artifacts,
            mod_name="test_mod",
            clean=True,
        )
        assert mod_dir.exists()
        assert (mod_dir / "main.lua").exists()
        assert (mod_dir / "scripts" / "common.lua").exists()
        assert (mod_dir / "scripts" / "data" / "data.lua").exists()
        assert (mod_dir / "metadata.xml").exists()

        # Verify content
        main_content = (mod_dir / "main.lua").read_text()
        assert "RegisterMod" in main_content
        assert 'include("scripts.common")' in main_content

    def test_build_legacy_flat_mode(self, tmp_path):
        from isaac_agent.build import ModBuilder
        from isaac_agent.core.state import GeneratedCode
        builder = ModBuilder(output_dir=str(tmp_path))
        artifacts = [
            GeneratedCode(
                scaffold_type="MOD_INIT",
                lua_code='local mod = RegisterMod("legacy", 1)',
            ),
        ]
        mod_dir = builder.build(
            artifacts=artifacts,
            mod_name="legacy_mod",
            clean=True,
        )
        assert mod_dir.exists()
        assert (mod_dir / "main.lua").exists()
        # Legacy mode writes all to main.lua
        content = (mod_dir / "main.lua").read_text()
        assert "legacy" in content


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
