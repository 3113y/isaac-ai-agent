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
        assert "CUSTOM_ITEM" in task.lua_scaffolds
        assert "AddCoins" in task.api_calls or "GetItemIdByName" in task.api_calls

    def test_fallback_parse_entity(self):
        agent = MainAgent()
        task = agent._fallback_parse("spawn a custom enemy that explodes on death")
        assert "CUSTOM_ENTITY" in task.lua_scaffolds
        assert "EntitySpawn" in task.api_calls or "SpawnExplosion" in task.api_calls

    def test_fallback_parse_unknown(self):
        agent = MainAgent()
        task = agent._fallback_parse("xyzzy foobar nothing")
        assert "RegisterMod" in task.api_calls
        assert len(task.lua_scaffolds) == 1
        assert task.lua_scaffolds[0] == "MC_POST_GAME_STARTED"

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


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
