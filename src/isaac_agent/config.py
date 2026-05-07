"""
Configuration management for Isaac AI Agent
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )
    """Application settings from environment variables"""
    
    # LLM Configuration (支持多个模型提供商)
    llm_provider: str = Field(default="openai", alias="LLM_PROVIDER")  # openai, glm, deepseek
    
    # OpenAI Configuration (GPT)
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo", alias="OPENAI_MODEL")
    
    # GLM Configuration (智谱/Qwen/通义千问)
    glm_api_key: Optional[str] = Field(default=None, alias="GLM_API_KEY")
    glm_model: str = Field(default="glm-4", alias="GLM_MODEL")
    
    # Deepseek Configuration
    deepseek_api_key: Optional[str] = Field(default=None, alias="DEEPSEEK_API_KEY")
    deepseek_model: str = Field(default="deepseek-chat", alias="DEEPSEEK_MODEL")
    
    # LLM Common Settings
    temperature: float = Field(default=0.7, alias="LLM_TEMPERATURE")
    max_tokens: int = Field(default=4096, alias="LLM_MAX_TOKENS")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_debug: bool = Field(default=False, alias="API_DEBUG")
    
    # Database Configuration
    faiss_index_path: str = Field(default="./data/isaac_api.faiss", alias="FAISS_INDEX_PATH")
    vector_db_type: str = Field(default="faiss", alias="VECTOR_DB_TYPE")
    rag_kb_path: str = Field(default="./processed_docs/rag_knowledge_base.json", alias="RAG_KB_PATH")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: str = Field(default="logs/isaac-agent.log", alias="LOG_FILE")
    
    # Isaac Mod Settings
    isaac_mod_dir: str = Field(default="./mods", alias="ISAAC_MOD_DIR")
    isaac_version: str = Field(default="1.7", alias="ISAAC_VERSION")
    lua_validator: str = Field(default="luacheck", alias="LUA_VALIDATOR")

    # Auto-detected paths (set at runtime, not from env)
    detected_mods_dir: str = ""
    detected_log_file: str = ""
    
    # Development
    dev_mode: bool = Field(default=False, alias="DEV_MODE")
    mock_api: bool = Field(default=True, alias="MOCK_API")


# Global settings instance
settings = Settings()
