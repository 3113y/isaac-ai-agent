"""
RAG Engine for Isaac API retrieval and search

DEPRECATED: This module is superseded by vector_rag.py and rag_bridge.py.
Use VectorRAG or RAGBridge from those modules instead.
"""

import warnings
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from loguru import logger
import json

warnings.warn(
    "isaac_api_search.py is deprecated. Use VectorRAG from vector_rag.py or "
    "RAGBridge from rag_bridge.py instead.",
    DeprecationWarning,
    stacklevel=2,
)


class IsaacAPISearchTool:
    """
    RAG-enabled search tool for Isaac API documentation
    
    This component:
    1. Searches API vectors (embeddings) for relevant functions
    2. Returns structured API references
    3. Provides examples and usage patterns
    
    Currently uses mock data; replace with real vector store (FAISS, Pinecone, etc.)
    """
    
    # Mock Isaac API database
    ISAAC_API_DATABASE = {
        "RegisterMod": {
            "category": "Mod Registration",
            "parameters": [
                {"name": "self", "type": "table"},
                {"name": "id", "type": "integer"},
                {"name": "name", "type": "string"},
            ],
            "return_type": "void",
            "description": "Register a new mod instance",
            "example_code": """
local isaac = require("isaac")
local mod = RegisterMod("MyMod", 1)
            """,
            "tags": ["initialization", "core"],
        },
        "OnEvent": {
            "category": "Event Hooks",
            "parameters": [
                {"name": "self", "type": "table"},
                {"name": "event_name", "type": "string"},
                {"name": "callback", "type": "function"},
            ],
            "return_type": "void",
            "description": "Register a callback for game events",
            "example_code": """
function mod:OnEvent(event, callback)
    -- Handle event
end
            """,
            "tags": ["events", "callbacks"],
        },
        "MC_POST_GAME_STARTED": {
            "category": "Callbacks",
            "parameters": [
                {"name": "continued", "type": "boolean"},
            ],
            "return_type": "void",
            "description": "Called after the game has started or loaded",
            "example_code": """
function mod:MC_POST_GAME_STARTED(continued)
    -- Code runs after game start
end
            """,
            "tags": ["lifecycle", "game-start"],
        },
        "AddCallback": {
            "category": "Callbacks",
            "parameters": [
                {"name": "self", "type": "table"},
                {"name": "callback", "type": "ModCallbacks"},
                {"name": "fn", "type": "function"},
            ],
            "return_type": "void",
            "description": "Add a callback to the mod",
            "example_code": """
mod:AddCallback(ModCallbacks.MC_POST_GAME_STARTED, function(continued)
    -- Event handler
end)
            """,
            "tags": ["callbacks", "event-system"],
        },
        "GetPlayer": {
            "category": "Entity Access",
            "parameters": [
                {"name": "index", "type": "integer", "optional": True},
            ],
            "return_type": "EntityPlayer",
            "description": "Get instance of the player entity",
            "example_code": """
local player = Isaac.GetPlayer(0)
local health = player.MaxHearts
            """,
            "tags": ["player", "entity"],
        },
    }
    
    def __init__(self, use_embeddings: bool = False):
        """
        Initialize the API search tool
        
        Args:
            use_embeddings: If True, use vector embeddings for similarity search
                          (requires FAISS or similar backend)
        """
        self.use_embeddings = use_embeddings
        self.database = self.ISAAC_API_DATABASE
        logger.info("🔧 IsaacAPISearchTool initialized")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Search the Isaac API database for matching functions
        
        Args:
            query: Search query (function name or description)
            top_k: Number of results to return
            
        Returns:
            List of matching API references
        """
        logger.info(f"🔍 Searching API for: {query}")
        
        results = []
        
        # Simple keyword matching (replace with vector search in production)
        query_lower = query.lower()
        
        for func_name, func_info in self.database.items():
            if (query_lower in func_name.lower() or
                query_lower in func_info.get("description", "").lower() or
                any(query_lower in tag for tag in func_info.get("tags", []))):
                
                results.append({
                    "function_name": func_name,
                    "category": func_info.get("category", "Unknown"),
                    "parameters": func_info.get("parameters", []),
                    "return_type": func_info.get("return_type", "void"),
                    "description": func_info.get("description", ""),
                    "example_code": func_info.get("example_code", ""),
                    "tags": func_info.get("tags", []),
                })
        
        # If no direct match, do fuzzy search
        if not results:
            logger.warning(f"⚠️  No direct match for '{query}', falling back to fuzzy search")
            results = self._fuzzy_search(query)
        
        logger.info(f"✅ Found {len(results[:top_k])} results")
        return results[:top_k]
    
    def _fuzzy_search(self, query: str, threshold: float = 0.6) -> List[Dict[str, Any]]:
        """
        Perform fuzzy search when direct keyword matching fails
        
        This is a placeholder for more sophisticated matching.
        In production, replace with proper vector similarity search (cosine similarity, etc.)
        """
        results = []
        
        # For demo: return related APIs
        related_apis = {
            "event": ["MC_POST_GAME_STARTED", "AddCallback"],
            "player": ["GetPlayer"],
            "register": ["RegisterMod"],
        }
        
        for keyword, apis in related_apis.items():
            if keyword in query.lower():
                for api_name in apis:
                    if api_name in self.database:
                        results.append({
                            "function_name": api_name,
                            "category": self.database[api_name].get("category", ""),
                            "parameters": self.database[api_name].get("parameters", []),
                            "return_type": self.database[api_name].get("return_type", "void"),
                            "description": self.database[api_name].get("description", ""),
                            "example_code": self.database[api_name].get("example_code", ""),
                            "tags": self.database[api_name].get("tags", []),
                        })
        
        return results
    
    def get_function_info(self, function_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific function"""
        if function_name not in self.database:
            logger.warning(f"⚠️  Function '{function_name}' not found in database")
            return None
        
        info = self.database[function_name]
        return {
            "function_name": function_name,
            "category": info.get("category", ""),
            "parameters": info.get("parameters", []),
            "return_type": info.get("return_type", "void"),
            "description": info.get("description", ""),
            "example_code": info.get("example_code", ""),
            "tags": info.get("tags", []),
        }
    
    def list_categories(self) -> List[str]:
        """List all available API categories"""
        categories = set()
        for func_info in self.database.values():
            categories.add(func_info.get("category", "Unknown"))
        return sorted(list(categories))
    
    def get_api_by_category(self, category: str) -> List[str]:
        """Get all APIs in a specific category"""
        return [
            func_name for func_name, func_info in self.database.items()
            if func_info.get("category") == category
        ]
    
    def export_schema(self) -> Dict[str, Any]:
        """Export complete API schema"""
        return {
            "version": "1.0",
            "total_apis": len(self.database),
            "categories": self.list_categories(),
            "apis": self.database,
        }
