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
    description="AI-powered mod code generation for The Binding of Isaac: Repentance",
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
        raise HTTPException(status_code=503, detail="Agent not initialized and no LLM provider specified")
    
    logger.info(f"📝 Received mod generation request: {request.user_input}")
    
    try:
        # Use specified LLM provider if provided, otherwise use default agent
        working_agent = agent
        
        if request.llm_provider:
            logger.info(f"🔄 Creating agent with {request.llm_provider} model")
            llm = init_llm(
                provider=request.llm_provider,
                model=request.llm_model,
                temperature=request.temperature,
            )
            if llm is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to initialize {request.llm_provider} LLM provider"
                )
            working_agent = MainAgent(llm=llm)
        
        if working_agent is None:
            raise HTTPException(status_code=503, detail="Agent not available")
        
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
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    return agent.get_workflow_info()


@app.get("/api/categories")
async def get_api_categories():
    """Get available API categories"""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    return {
        "categories": agent.api_search_tool.list_categories()
    }


@app.get("/templates")
async def get_templates():
    """List all available Lua templates"""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    return {
        "templates": agent.template_manager.list_templates(),
        "stats": agent.template_manager.get_template_stats(),
    }


@app.get("/templates/{template_name}")
async def get_template(template_name: str):
    """Get a specific template"""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    if not agent.template_manager.validate_template(template_name):
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found")
    
    return {
        "name": template_name,
        "description": agent.template_manager.get_template_description(template_name),
        "code": agent.template_manager.get_template(template_name),
    }


@app.get("/api/search")
async def search_api(query: str):
    """Search Isaac API"""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    results = agent.api_search_tool.search(query)
    return {"query": query, "results": results}


# Health check on startup
@app.on_event("startup")
async def startup_event():
    """Startup event"""
    logger.info("API server starting up")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event"""
    logger.info("API server shutting down")
