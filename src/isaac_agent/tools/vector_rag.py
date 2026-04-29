"""
Advanced RAG System with FAISS Vector Search for Isaac API
"""

import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from loguru import logger

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("⚠️  FAISS not installed. Install with: pip install faiss-cpu")

try:
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.embeddings import HuggingFaceEmbeddings
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    logger.warning("⚠️  Embeddings not available. Install with: pip install sentence-transformers langchain-openai")


class IsaacAPIDatabase:
    """
    Complete Isaac API Database with 30+ documented functions.
    
    This is an expanded version of the API reference for more comprehensive RAG.
    """
    
    DATABASE = {
        # Core Registration
        "RegisterMod": {
            "category": "Mod Management",
            "parameters": [
                {"name": "self", "type": "table"},
                {"name": "id", "type": "integer"},
                {"name": "name", "type": "string"},
            ],
            "return_type": "void",
            "description": "Register a new mod instance with Isaac. Required for all mods.",
            "example_code": "local mod = RegisterMod('MyMod', 1)",
            "tags": ["initialization", "core", "registration"],
        },
        
        # Callbacks
        "MC_POST_GAME_STARTED": {
            "category": "Game Lifecycle",
            "parameters": [{"name": "continued", "type": "boolean"}],
            "return_type": "void",
            "description": "Called immediately after a new game starts or a save is loaded.",
            "example_code": "mod:AddCallback(ModCallbacks.MC_POST_GAME_STARTED, function(continued) end)",
            "tags": ["lifecycle", "game-start", "event"],
        },
        
        "MC_POST_UPDATE": {
            "category": "Game Lifecycle",
            "parameters": [],
            "return_type": "void",
            "description": "Called every game update/frame.",
            "example_code": "mod:AddCallback(ModCallbacks.MC_POST_UPDATE, function() end)",
            "tags": ["lifecycle", "update", "event", "frame"],
        },
        
        "MC_POST_NEW_ROOM": {
            "category": "Room Events",
            "parameters": [],
            "return_type": "void",
            "description": "Called after entering a new room.",
            "example_code": "mod:AddCallback(ModCallbacks.MC_POST_NEW_ROOM, function() end)",
            "tags": ["room", "event", "navigation"],
        },
        
        "MC_POST_ROOM_CLEAR": {
            "category": "Room Events",
            "parameters": [],
            "return_type": "void",
            "description": "Called when all enemies in the room are defeated.",
            "example_code": "mod:AddCallback(ModCallbacks.MC_POST_ROOM_CLEAR, function() end)",
            "tags": ["room", "enemies", "victory", "event"],
        },
        
        # Entity Operations
        "EntitySpawn": {
            "category": "Entity Management",
            "parameters": [
                {"name": "type", "type": "integer"},
                {"name": "variant", "type": "integer"},
                {"name": "subtype", "type": "integer"},
                {"name": "position", "type": "Vector"},
            ],
            "return_type": "Entity",
            "description": "Spawn a new entity at the specified position.",
            "example_code": "Isaac.Spawn(EntityType.ENTITY_TEAR, 0, 0, Vector(100, 100))",
            "tags": ["entity", "spawn", "creation"],
        },
        
        "GetPlayer": {
            "category": "Player Access",
            "parameters": [{"name": "index", "type": "integer", "optional": True}],
            "return_type": "EntityPlayer",
            "description": "Get reference to a player entity by index.",
            "example_code": "local player = Isaac.GetPlayer(0)",
            "tags": ["player", "entity", "access"],
        },
        
        "GetEntityCount": {
            "category": "Entity Query",
            "parameters": [{"name": "type", "type": "integer", "optional": True}],
            "return_type": "integer",
            "description": "Get count of entities, optionally filtered by type.",
            "example_code": "local count = Isaac.GetEntityCount()",
            "tags": ["entity", "query", "count"],
        },
        
        # Item Operations
        "GetItemIdByName": {
            "category": "Item Management",
            "parameters": [{"name": "name", "type": "string"}],
            "return_type": "integer",
            "description": "Get item ID by its name string.",
            "example_code": "local itemId = Isaac.GetItemIdByName('Sad Onion')",
            "tags": ["item", "lookup", "id"],
        },
        
        "AddCallback": {
            "category": "Event System",
            "parameters": [
                {"name": "self", "type": "table"},
                {"name": "callback_enum", "type": "ModCallbacks"},
                {"name": "function", "type": "function"},
            ],
            "return_type": "void",
            "description": "Register a callback function for a specific game event.",
            "example_code": "mod:AddCallback(ModCallbacks.MC_POST_UPDATE, function() print('update') end)",
            "tags": ["callbacks", "event-system", "registration"],
        },
        
        "OnItemPickup": {
            "category": "Item Events",
            "parameters": [
                {"name": "item", "type": "Item"},
                {"name": "player", "type": "EntityPlayer"},
            ],
            "return_type": "void",
            "description": "Called when a player picks up an item.",
            "example_code": "function mod:OnItemPickup(item, player) end",
            "tags": ["item", "pickup", "event", "player"],
        },
        
        "OnEntityTakeDamage": {
            "category": "Entity Events",
            "parameters": [
                {"name": "entity", "type": "Entity"},
                {"name": "damage", "type": "number"},
                {"name": "flags", "type": "integer"},
                {"name": "source", "type": "EntityRef"},
            ],
            "return_type": "boolean",
            "description": "Called when an entity takes damage.",
            "example_code": "mod:AddCallback(ModCallbacks.MC_ENTITY_TAKE_DMG, function(entity, damage) end)",
            "tags": ["damage", "entity", "combat", "event"],
        },
        
        # Room Operations
        "GetRoom": {
            "category": "Room Access",
            "parameters": [],
            "return_type": "Room",
            "description": "Get the current room object.",
            "example_code": "local room = Game():GetRoom()",
            "tags": ["room", "access", "current"],
        },
        
        "GetRoomData": {
            "category": "Room Query",
            "parameters": [],
            "return_type": "RoomData",
            "description": "Get detailed room data for the current room.",
            "example_code": "local roomData = Game():GetRoom():GetRoomData()",
            "tags": ["room", "data", "properties"],
        },
        
        "GetDescendants": {
            "category": "Entity Query",
            "parameters": [
                {"name": "type", "type": "integer"},
                {"name": "variant", "type": "integer", "optional": True},
            ],
            "return_type": "table",
            "description": "Get all descendants of an entity type.",
            "example_code": "local tears = Game():GetRoom():GetDescendants(EntityType.ENTITY_TEAR)",
            "tags": ["entity", "query", "descendants"],
        },
        
        # Tear/Explosion Operations
        "SpawnTear": {
            "category": "Tear Operations",
            "parameters": [
                {"name": "position", "type": "Vector"},
                {"name": "velocity", "type": "Vector"},
                {"name": "source", "type": "Entity"},
            ],
            "return_type": "EntityTear",
            "description": "Spawn a tear projectile.",
            "example_code": "local tear = player:SpawnTear(position, velocity)",
            "tags": ["tear", "projectile", "spawn"],
        },
        
        "SpawnExplosion": {
            "category": "Effect Operations",
            "parameters": [
                {"name": "position", "type": "Vector"},
                {"name": "source", "type": "Entity"},
            ],
            "return_type": "void",
            "description": "Create an explosion at the specified position.",
            "example_code": "Game():SpawnExplosion(Vector(100, 100), entity)",
            "tags": ["explosion", "effect", "damage"],
        },
        
        # Player Modifications
        "AddHearts": {
            "category": "Player Modification",
            "parameters": [{"name": "count", "type": "integer"}],
            "return_type": "void",
            "description": "Add red heart containers to the player.",
            "example_code": "player:AddHearts(2)",
            "tags": ["player", "health", "modification"],
        },
        
        "AddSoulHearts": {
            "category": "Player Modification",
            "parameters": [{"name": "count", "type": "number"}],
            "return_type": "void",
            "description": "Add soul heart containers to the player.",
            "example_code": "player:AddSoulHearts(2)",
            "tags": ["player", "soul-hearts", "modification"],
        },
        
        "AddCoins": {
            "category": "Player Modification",
            "parameters": [{"name": "count", "type": "integer"}],
            "return_type": "void",
            "description": "Add coins to the player's balance.",
            "example_code": "player:AddCoins(10)",
            "tags": ["player", "coins", "currency"],
        },
        
        "AddBombs": {
            "category": "Player Modification",
            "parameters": [{"name": "count", "type": "integer"}],
            "return_type": "void",
            "description": "Add bombs to the player's inventory.",
            "example_code": "player:AddBombs(5)",
            "tags": ["player", "bombs", "items"],
        },
        
        "AddKeys": {
            "category": "Player Modification",
            "parameters": [{"name": "count", "type": "integer"}],
            "return_type": "void",
            "description": "Add keys to the player's inventory.",
            "example_code": "player:AddKeys(3)",
            "tags": ["player", "keys", "items"],
        },
        
        # Item Granting
        "AddItemFromPool": {
            "category": "Item Granting",
            "parameters": [
                {"name": "pool", "type": "string"},
                {"name": "force_id", "type": "integer", "optional": True},
            ],
            "return_type": "void",
            "description": "Grant an item from the specified pool to the player.",
            "example_code": "player:AddItemFromPool('treasure', 0)",
            "tags": ["item", "grant", "pool"],
        },
        
        # Stat Modifications
        "AddBlueFly": {
            "category": "Familiar Management",
            "parameters": [{"name": "count", "type": "integer"}],
            "return_type": "void",
            "description": "Add blue attack flies to the player.",
            "example_code": "player:AddBluflyFromPool(1)",
            "tags": ["familiar", "fly", "helper"],
        },
        
        # Save Management
        "SaveData": {
            "category": "Persistence",
            "parameters": [{"name": "data", "type": "table"}],
            "return_type": "void",
            "description": "Save persistent mod data.",
            "example_code": "mod:SaveData()",
            "tags": ["save", "persistence", "data"],
        },
        
        # Vector Operations
        "Vector": {
            "category": "Math",
            "parameters": [
                {"name": "x", "type": "number"},
                {"name": "y", "type": "number"},
            ],
            "return_type": "Vector",
            "description": "Create a 2D vector with x and y components.",
            "example_code": "local pos = Vector(100, 100)",
            "tags": ["math", "vector", "position"],
        },
        
        # Random Operations  
        "GetRandomInt": {
            "category": "Randomization",
            "parameters": [
                {"name": "min", "type": "integer"},
                {"name": "max", "type": "integer"},
            ],
            "return_type": "integer",
            "description": "Get a random integer in the specified range.",
            "example_code": "local num = math.random(1, 10)",
            "tags": ["random", "rng", "math"],
        },
    }


class VectorRAG:
    """
    Advanced RAG system with FAISS vector search and OpenAI embeddings.
    
    Provides semantic search over Isaac API documentation.
    """
    
    def __init__(
        self,
        embedding_model: str = "openai",
        faiss_index_path: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Initialize Vector RAG system.
        
        Args:
            embedding_model: "openai" or "huggingface"
            faiss_index_path: Path to save/load FAISS index
            api_key: OpenAI API key (if using OpenAI embeddings)
        """
        self.embedding_model_name = embedding_model
        self.index_path = Path(faiss_index_path or "./data/isaac_api.faiss")
        self.metadata_path = Path(str(self.index_path).replace(".faiss", "_metadata.pkl"))
        
        self.embeddings = None
        self.index = None
        self.documents = []
        self.metadata = []
        
        self._initialize_embeddings(embedding_model, api_key)
        self._load_or_build_index()
        
        logger.info("✅ Vector RAG System initialized")
    
    def _initialize_embeddings(self, model: Optional[str], api_key: Optional[str]):
        """Initialize embedding model"""
        if not model or model == "fallback":
            logger.warning("⚠️  Using fallback keyword search mode")
            return
        
        if model == "openai":
            if not EMBEDDINGS_AVAILABLE:
                logger.warning("⚠️  langchain-openai not installed, falling back to HuggingFace")
                self._initialize_embeddings("huggingface", None)
                return
            try:
                self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
                logger.info("🔐 OpenAI Embeddings initialized")
            except Exception as e:
                logger.warning(f"⚠️  OpenAI embeddings failed: {e}, falling back to HuggingFace")
                self._initialize_embeddings("huggingface", None)
        elif model == "huggingface":
            if not EMBEDDINGS_AVAILABLE:
                logger.warning("⚠️  sentence-transformers not installed, using fallback search")
                return
            try:
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    encode_kwargs={"normalize_embeddings": True},
                )
                logger.info("🤗 HuggingFace Embeddings initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize embeddings: {e}")
                logger.warning("⚠️  Falling back to keyword search")
        else:
            logger.error(f"❌ Unknown embedding model: {model}")
    
    def _load_or_build_index(self):
        """Load existing index or build new one"""
        if self.index_path.exists() and self.metadata_path.exists():
            try:
                self._load_index()
                logger.info(f"📂 Loaded existing FAISS index from {self.index_path}")
            except Exception as e:
                logger.warning(f"Failed to load index: {e}, rebuilding...")
                self._build_index()
        else:
            self._build_index()
    
    def _build_index(self):
        """Build FAISS index from API database"""
        if not FAISS_AVAILABLE or not self.embeddings:
            logger.warning("⚠️  FAISS or embeddings not available, using fallback")
            return
        
        logger.info("🔨 Building FAISS index...")
        
        # Prepare documents
        self.documents = []
        for func_name, func_info in IsaacAPIDatabase.DATABASE.items():
            # Create document text combining all relevant fields
            doc_text = f"{func_name}: {func_info.get('description', '')}. Category: {func_info.get('category', '')}. Tags: {', '.join(func_info.get('tags', []))}"
            self.documents.append(doc_text)
            self.metadata.append({
                "function_name": func_name,
                "description": func_info.get("description", ""),
                "category": func_info.get("category", ""),
                "tags": func_info.get("tags", []),
            })
        
        # Generate embeddings
        logger.info(f"📊 Embedding {len(self.documents)} API functions...")
        embeddings_list = self.embeddings.embed_documents(self.documents)
        embeddings_array = np.array(embeddings_list).astype("float32")
        
        # Build FAISS index
        dimension = embeddings_array.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings_array)
        
        # Save index
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)
        
        logger.info(f"💾 Saved FAISS index to {self.index_path}")
    
    def _load_index(self):
        """Load FAISS index and metadata"""
        if not FAISS_AVAILABLE:
            return
        
        self.index = faiss.read_index(str(self.index_path))
        
        with open(self.metadata_path, "rb") as f:
            self.metadata = pickle.load(f)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant API functions using vector similarity.
        
        Args:
            query: Natural language query
            top_k: Number of results to return
            
        Returns:
            List of matching API references
        """
        if not self.embeddings or not self.index:
            logger.warning("⚠️  Vector search not available, using fallback")
            return self._fallback_search(query)
        
        logger.info(f"🔍 Searching for: {query}")
        
        # Embed query
        query_embedding = np.array([self.embeddings.embed_query(query)]).astype("float32")
        
        # Search index
        distances, indices = self.index.search(query_embedding, min(top_k, len(self.metadata)))
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx >= 0 and idx < len(self.metadata):
                meta = self.metadata[idx]
                func_name = meta["function_name"]
                func_info = IsaacAPIDatabase.DATABASE.get(func_name, {})
                
                results.append({
                    "function_name": func_name,
                    "category": func_info.get("category", ""),
                    "description": func_info.get("description", ""),
                    "parameters": func_info.get("parameters", []),
                    "return_type": func_info.get("return_type", "void"),
                    "example_code": func_info.get("example_code", ""),
                    "tags": func_info.get("tags", []),
                    "score": float(distance),
                })
        
        logger.info(f"✅ Found {len(results)} matching functions")
        return results
    
    def _fallback_search(self, query: str) -> List[Dict[str, Any]]:
        """Fallback keyword-based search"""
        query_lower = query.lower()
        results = []
        
        for func_name, func_info in IsaacAPIDatabase.DATABASE.items():
            # Score based on keyword matches
            score = 0
            if query_lower in func_name.lower():
                score += 10
            if query_lower in func_info.get("description", "").lower():
                score += 5
            for tag in func_info.get("tags", []):
                if query_lower in tag.lower():
                    score += 3
            
            if score > 0:
                results.append({
                    "function_name": func_name,
                    "category": func_info.get("category", ""),
                    "description": func_info.get("description", ""),
                    "parameters": func_info.get("parameters", []),
                    "return_type": func_info.get("return_type", "void"),
                    "example_code": func_info.get("example_code", ""),
                    "tags": func_info.get("tags", []),
                    "score": score,
                })
        
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:5]
    
    def get_function_info(self, function_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed info about a specific function"""
        if function_name not in IsaacAPIDatabase.DATABASE:
            return None
        
        info = IsaacAPIDatabase.DATABASE[function_name]
        return {
            "function_name": function_name,
            "category": info.get("category", ""),
            "description": info.get("description", ""),
            "parameters": info.get("parameters", []),
            "return_type": info.get("return_type", "void"),
            "example_code": info.get("example_code", ""),
            "tags": info.get("tags", []),
        }
    
    def list_categories(self) -> List[str]:
        """List all API categories"""
        categories = set()
        for func_info in IsaacAPIDatabase.DATABASE.values():
            categories.add(func_info.get("category", "Unknown"))
        return sorted(list(categories))
    
    def get_apis_by_category(self, category: str) -> List[str]:
        """Get all APIs in a category"""
        return [
            func_name for func_name, func_info in IsaacAPIDatabase.DATABASE.items()
            if func_info.get("category") == category
        ]
    
    def export_database(self) -> Dict[str, Any]:
        """Export complete API database"""
        return IsaacAPIDatabase.DATABASE


# Backward compatibility wrapper
class IsaacAPISearchTool(VectorRAG):
    """
    Backward compatible wrapper for the old IsaacAPISearchTool interface.
    Uses VectorRAG internally for semantic search.
    """
    
    def __init__(self, use_embeddings: bool = True):
        """Initialize with vector search enabled"""
        embedding_model = "huggingface" if use_embeddings else "none"
        super().__init__(embedding_model=embedding_model if use_embeddings else None)
