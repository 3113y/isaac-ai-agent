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


class TestVectorRAG:
    """Test advanced RAG with vector search"""
    
    def test_tool_initialization(self):
        """Test tool initializes"""
        tool = VectorRAG(embedding_model="huggingface")
        assert tool is not None
    
    def test_search_by_query(self):
        """Test semantic search"""
        tool = VectorRAG(embedding_model="huggingface")
        results = tool.search("player health modification", top_k=3)
        assert len(results) > 0
        assert "function_name" in results[0]
    
    def test_get_function_info(self):
        """Test getting specific function info"""
        tool = VectorRAG(embedding_model="huggingface")
        info = tool.get_function_info("GetPlayer")
        assert info is not None
        assert info["category"] == "Player Access"
    
    def test_list_categories(self):
        """Test listing categories"""
        tool = VectorRAG(embedding_model="huggingface")
        categories = tool.list_categories()
        assert len(categories) > 0
        assert "Player Access" in categories
    
    def test_api_database(self):
        """Test API database"""
        db = IsaacAPIDatabase.DATABASE
        assert "GetPlayer" in db
        assert len(db) >= 30  # Check for expanded database
    
    def test_fallback_search(self):
        """Test fallback keyword search"""
        tool = VectorRAG(embedding_model=None)
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
        assert result.session_id is not None
        assert result.stage in [WorkflowStage.COMPLETE, WorkflowStage.ERROR]


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
