"""
FastAPI application for Isaac AI Agent
"""

from contextlib import asynccontextmanager
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loguru import logger

from isaac_agent.core.agent import MainAgent
from isaac_agent.core.state import WorkflowStage, GeneratedCode
from isaac_agent.config import settings
from isaac_agent.llm_factory import init_llm


# Pydantic models for API
class ModRequest(BaseModel):
    """Request model for mod generation"""
    user_input: str
    session_id: Optional[str] = None
    llm_provider: Optional[str] = None  # openai, glm, deepseek (optional)
    llm_model: Optional[str] = None  # specific model name like gpt-4-turbo
    llm_api_key: Optional[str] = None  # user's own API key
    temperature: Optional[float] = None  # LLM temperature


class CodeArtifact(BaseModel):
    """Generated code artifact"""
    scaffold_type: str
    lua_code: str
    imports: List[str] = []
    dependencies: List[str] = []


class ModResponse(BaseModel):
    """Response model for mod generation"""
    session_id: str
    status: str
    stage: str
    generated_code: List[CodeArtifact] = []
    messages: List[dict] = []
    errors: List[str] = []


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    agent_ready: bool
    version: str


# Initialize agent (will be set in lifespan)
agent: Optional[MainAgent] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    global agent
    
    # Startup
    logger.info("🚀 Starting Isaac AI Agent API")
    try:
        agent = MainAgent()
        logger.info("✅ Agent initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize agent: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Isaac AI Agent API")


# Create FastAPI app
app = FastAPI(
    title="Isaac AI Agent API",
    description="AI 驱动的《以撒的结合：忏悔》Mod 代码生成",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        agent_ready=agent is not None,
        version="0.1.0",
    )


@app.post("/generate", response_model=ModResponse)
async def generate_mod(request: ModRequest):
    """
    Generate mod code from natural language request
    
    Args:
        request: ModRequest containing user input and optional LLM settings
        
    Returns:
        ModResponse with generated code artifacts
    """
    if agent is None and not request.llm_provider:
        raise HTTPException(status_code=503, detail="智能体未初始化且未指定 LLM 提供商")
    
    logger.info(f"📝 Received mod generation request: {request.user_input}")
    
    try:
        # Use specified LLM provider if provided, otherwise use default agent
        working_agent = agent

        if request.llm_provider:
            logger.info(f"Creating agent with {request.llm_provider} model")
            llm = init_llm(
                provider=request.llm_provider,
                model=request.llm_model,
                api_key=request.llm_api_key,
                temperature=request.temperature,
            )
            if llm is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"无法初始化 {request.llm_provider} LLM 提供商"
                )
            working_agent = MainAgent(llm=llm)
        
        if working_agent is None:
            raise HTTPException(status_code=503, detail="智能体不可用")
        
        # Run the workflow
        result = await working_agent.run(request.user_input)
        
        # Convert to response
        code_artifacts = [
            CodeArtifact(
                scaffold_type=code.scaffold_type,
                lua_code=code.lua_code,
                imports=code.imports,
                dependencies=code.dependencies,
            )
            for code in result.generated_code
        ]
        
        response = ModResponse(
            session_id=result.session_id,
            status="success" if result.stage == WorkflowStage.COMPLETE else "partial",
            stage=result.stage.value,
            generated_code=code_artifacts,
            messages=result.messages,
            errors=result.errors,
        )
        
        logger.info(f"✅ Generated mod for session {result.session_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error during mod generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/info")
async def get_agent_info():
    """Get information about the agent"""
    if agent is None:
        raise HTTPException(status_code=503, detail="智能体未初始化")

    info = agent.get_workflow_info()
    info["detected_mods_dir"] = str(agent.mods_dir) if agent.mods_dir else None
    info["detected_log_file"] = str(agent.log_file) if agent.log_file else None
    return info


@app.get("/api/categories")
async def get_api_categories():
    """Get available API categories"""
    if agent is None:
        raise HTTPException(status_code=503, detail="智能体未初始化")
    
    return {
        "categories": agent.api_search_tool.list_categories()
    }


@app.get("/templates")
async def get_templates():
    """List all available Lua templates"""
    if agent is None:
        raise HTTPException(status_code=503, detail="智能体未初始化")
    
    return {
        "templates": agent.template_manager.list_templates(),
        "stats": agent.template_manager.get_template_stats(),
    }


@app.get("/templates/{template_name}")
async def get_template(template_name: str):
    """Get a specific template"""
    if agent is None:
        raise HTTPException(status_code=503, detail="智能体未初始化")
    
    if not agent.template_manager.validate_template(template_name):
        raise HTTPException(status_code=404, detail=f"模板 '{template_name}' 未找到")
    
    return {
        "name": template_name,
        "description": agent.template_manager.get_template_description(template_name),
        "code": agent.template_manager.get_template(template_name),
    }


@app.get("/api/search")
async def search_api(query: str):
    """Search Isaac API"""
    if agent is None:
        raise HTTPException(status_code=503, detail="智能体未初始化")

    results = agent.api_search_tool.search(query)
    return {"query": query, "results": results}


class LogAnalyzeRequest(BaseModel):
    """Request model for log error analysis"""
    source_code: str = ""
    mod_name: str = "isaac_mod"


@app.post("/log/analyze")
async def analyze_log(request: LogAnalyzeRequest):
    """Analyze the Isaac log file for Lua errors and suggest fixes."""
    if agent is None:
        raise HTTPException(status_code=503, detail="智能体未初始化")

    try:
        analysis = agent.analyze_log_errors(
            source_code=request.source_code,
            mod_name=request.mod_name,
        )
        return analysis
    except Exception as e:
        logger.error(f"Log analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/paths")
async def get_detected_paths():
    """Get auto-detected Isaac paths (mods dir + log file)."""
    if agent is None:
        raise HTTPException(status_code=503, detail="智能体未初始化")

    return {
        "mods_dir": str(agent.mods_dir) if agent.mods_dir else None,
        "log_file": str(agent.log_file) if agent.log_file else None,
    }


