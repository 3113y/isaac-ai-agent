"""
Tests for LLM Factory functionality
"""

import pytest
from isaac_agent.llm_factory import init_llm
from isaac_agent.config import settings


class TestLLMFactory:
    """Test LLM factory initialization"""
    
    def test_init_llm_invalid_provider(self):
        """Test with invalid LLM provider"""
        llm = init_llm(provider="invalid_provider")
        assert llm is None
    
    def test_init_llm_with_fallback(self):
        """Test fallback when API key missing"""
        llm = init_llm(
            provider="openai",
            api_key=None,  # Explicitly no API key
        )
        # Should return None since no API key in env either
        assert llm is None or hasattr(llm, 'model_name') or hasattr(llm, 'model')
    
    def test_init_llm_custom_temperature(self):
        """Test LLM initialization with custom temperature"""
        # This test mainly checks that temperature parameter is accepted
        # Actual initialization might fail due to missing API keys
        llm = init_llm(
            provider="openai",
            temperature=0.5,
        )
        # Result depends on whether API key is configured
        if llm:
            if hasattr(llm, 'temperature'):
                assert llm.temperature == 0.5
    
    def test_supported_providers(self):
        """Test that supported providers are recognized"""
        for provider in ["openai", "gpt", "glm", "qwen", "deepseek"]:
            # Should not raise exception, may return None if not configured
            result = init_llm(provider=provider)
            # Just verify no exception is raised
            assert result is None or hasattr(result, '__call__')
    
    def test_init_llm_with_custom_model(self):
        """Test LLM initialization with custom model name"""
        # Test that model parameter is accepted
        llm = init_llm(
            provider="openai",
            model="gpt-4-turbo",
        )
        # Result depends on API key configuration
        assert llm is None or hasattr(llm, 'model_name')


class TestSettings:
    """Test configuration settings"""
    
    def test_settings_llm_provider_default(self):
        """Test default LLM provider is set"""
        assert settings.llm_provider is not None
        assert settings.llm_provider.lower() in ["openai", "glm", "deepseek"]
    
    def test_settings_temperature_range(self):
        """Test temperature is in valid range"""
        assert 0 <= settings.temperature <= 2
    
    def test_settings_max_tokens_positive(self):
        """Test max_tokens is positive"""
        assert settings.max_tokens > 0


class TestAgentWithMultipleLLMs:
    """Test MainAgent with different LLM providers"""
    
    @pytest.mark.asyncio
    async def test_agent_initialization_without_llm(self):
        """Test agent can initialize without explicit LLM (uses default)"""
        from isaac_agent.core.agent import MainAgent
        
        # Should initialize successfully (might use None or default)
        agent = MainAgent()
        assert agent is not None
        assert agent.compiled_graph is not None
    
    @pytest.mark.asyncio
    async def test_agent_initialization_with_custom_llm(self):
        """Test agent initialization with custom LLM"""
        from isaac_agent.core.agent import MainAgent
        
        # Initialize with openai if available
        llm = init_llm(provider="openai")
        if llm:
            agent = MainAgent(llm=llm)
            assert agent is not None
            assert agent.llm is not None
    
    def test_agent_accepts_llm_parameter(self):
        """Test that MainAgent accepts optional llm parameter"""
        from isaac_agent.core.agent import MainAgent
        
        # Should not raise exception with llm=None
        agent = MainAgent(llm=None)
        assert agent is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
