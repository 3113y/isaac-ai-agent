"""
LLM Factory - Initialize language models from different providers
Supports: OpenAI (GPT), GLM (Qwen/智谱), Deepseek
"""

from typing import Optional
from loguru import logger
from langchain_core.language_model.base import BaseLanguageModel

from isaac_agent.config import settings


def _init_openai_llm(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> BaseLanguageModel:
    """Initialize OpenAI ChatGPT model"""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        raise ImportError("Install: pip install langchain-openai")
    
    api_key = api_key or settings.openai_api_key
    if not api_key:
        raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY env var")
    
    model = model or settings.openai_model
    temperature = temperature if temperature is not None else settings.temperature
    max_tokens = max_tokens or settings.max_tokens
    
    logger.info(f"🤖 Initializing OpenAI ChatGPT: {model}")
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def _init_glm_llm(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> BaseLanguageModel:
    """Initialize GLM model (智谱/Qwen/通义千问)"""
    try:
        from langchain_community.chat_models.zhipuai import ChatZhipuAI
    except ImportError:
        # Fallback to LangChain integration if available
        try:
            from langchain_openai import ChatOpenAI
            logger.warning("⚠️  langchain-community not installed, using OpenAI mock")
            return _init_openai_llm(api_key, model, temperature, max_tokens)
        except ImportError:
            raise ImportError("Install: pip install langchain-community langchain-openai")
    
    api_key = api_key or settings.glm_api_key
    if not api_key:
        raise ValueError("GLM API key not provided. Set GLM_API_KEY env var")
    
    model = model or settings.glm_model
    temperature = temperature if temperature is not None else settings.temperature
    max_tokens = max_tokens or settings.max_tokens
    
    logger.info(f"🤖 Initializing GLM/Qwen: {model}")
    return ChatZhipuAI(
        api_key=api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def _init_deepseek_llm(
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> BaseLanguageModel:
    """Initialize Deepseek model"""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        raise ImportError("Install: pip install langchain-openai")
    
    api_key = api_key or settings.deepseek_api_key
    if not api_key:
        raise ValueError("Deepseek API key not provided. Set DEEPSEEK_API_KEY env var")
    
    model = model or settings.deepseek_model
    temperature = temperature if temperature is not None else settings.temperature
    max_tokens = max_tokens or settings.max_tokens
    
    logger.info(f"🤖 Initializing Deepseek: {model}")
    # Deepseek compatible with OpenAI API
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url="https://api.deepseek.com/v1",
        temperature=temperature,
        max_tokens=max_tokens,
    )


def init_llm(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> Optional[BaseLanguageModel]:
    """
    Initialize LLM from provider
    
    Args:
        provider: LLM provider ("openai", "glm", "deepseek")
        model: Model name to use
        api_key: API key for the provider
        temperature: Temperature for sampling
        max_tokens: Max tokens to generate
    
    Returns:
        BaseLanguageModel instance or None if provider not configured
    """
    provider = provider or settings.llm_provider
    
    if not provider:
        logger.warning("⚠️  No LLM provider configured")
        return None
    
    provider = provider.lower().strip()
    
    try:
        if provider == "openai" or provider == "gpt":
            return _init_openai_llm(api_key, model, temperature, max_tokens)
        elif provider == "glm" or provider == "qwen":
            return _init_glm_llm(api_key, model, temperature, max_tokens)
        elif provider == "deepseek":
            return _init_deepseek_llm(api_key, model, temperature, max_tokens)
        else:
            logger.error(f"❌ Unknown LLM provider: {provider}")
            logger.info("✅ Supported providers: openai, glm, deepseek")
            return None
    except Exception as e:
        logger.error(f"❌ Failed to initialize {provider} LLM: {e}")
        return None
