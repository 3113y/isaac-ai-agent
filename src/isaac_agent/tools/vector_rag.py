"""
Advanced RAG System with FAISS Vector Search for Isaac API
"""

import json
import os
import pickle
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
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
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False

try:
    from langchain_huggingface import HuggingFaceEmbeddings
    HF_EMBEDDINGS_AVAILABLE = True
except ImportError:
    HF_EMBEDDINGS_AVAILABLE = False
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        HF_EMBEDDINGS_AVAILABLE = True
    except ImportError:
        HF_EMBEDDINGS_AVAILABLE = False


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
    Supports external document sources (from knowledge base) or falls back
    to the built-in IsaacAPIDatabase.
    """

    def __init__(
        self,
        embedding_model: str = "openai",
        faiss_index_path: Optional[str] = None,
        api_key: Optional[str] = None,
        documents: Optional[List[Tuple[str, Dict[str, Any]]]] = None,
    ):
        """
        Initialize Vector RAG system.

        Args:
            embedding_model: "openai" or "huggingface"
            faiss_index_path: Path to save/load FAISS index
            api_key: OpenAI API key (if using OpenAI embeddings)
            documents: Optional list of (doc_text, metadata) pairs from an external source.
                       When provided, these are indexed instead of IsaacAPIDatabase.DATABASE.
        """
        self.embedding_model_name = embedding_model
        self.index_path = Path(faiss_index_path or "./data/isaac_api.faiss")
        self.metadata_path = Path(str(self.index_path).replace(".faiss", "_metadata.pkl"))

        self.embeddings = None
        self.index = None
        self.documents = []
        self.metadata = []

        # External documents take priority over the built-in database
        self._external_documents = documents

        # Lazy-init state: embeddings are loaded on first search(), not at construction
        self._embeddings_config = (embedding_model, api_key)
        self._embeddings_initialized = False
        self._embeddings_lock = threading.Lock()
        self._index_built = False

        # Load existing FAISS index from disk eagerly (fast, no embeddings needed)
        # If index doesn't exist yet, prepare documents but defer index building
        self._load_or_build_index()

        logger.info("✅ Vector RAG System initialized (embeddings deferred)")

    def _ensure_embeddings(self) -> bool:
        """Lazily initialize embeddings on first use. Thread-safe. Returns True if ready."""
        if self._embeddings_initialized:
            return self.embeddings is not None

        with self._embeddings_lock:
            if self._embeddings_initialized:
                return self.embeddings is not None

            model, api_key = self._embeddings_config
            self._initialize_embeddings(model, api_key)

            # If embeddings are now ready and we have documents but no index, build it
            if self.embeddings is not None and not self._index_built and self.documents:
                self._build_index()
                self._index_built = True

            self._embeddings_initialized = True
            return self.embeddings is not None

    def _init_hf_embeddings_offline(self) -> bool:
        """Try initializing HuggingFaceEmbeddings without network (cached model)."""
        try:
            prior = os.environ.get("HF_HUB_OFFLINE")
            os.environ["HF_HUB_OFFLINE"] = "1"
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                encode_kwargs={"normalize_embeddings": True},
            )
            return True
        except Exception:
            self.embeddings = None
            return False
        finally:
            if prior is not None:
                os.environ["HF_HUB_OFFLINE"] = prior
            else:
                os.environ.pop("HF_HUB_OFFLINE", None)

    def _init_hf_embeddings_online(self) -> bool:
        """Try initializing HuggingFaceEmbeddings with network, guarded by a 60s timeout."""
        def _create():
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                encode_kwargs={"normalize_embeddings": True},
            )

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_create)
            try:
                self.embeddings = future.result(timeout=60)
                return True
            except FutureTimeoutError:
                logger.error("❌ Embeddings initialization timed out after 60s")
                self.embeddings = None
                return False
            except Exception as e:
                logger.error(f"❌ Failed to initialize embeddings: {e}")
                self.embeddings = None
                return False

    def _initialize_embeddings(self, model: Optional[str], api_key: Optional[str]):
        """Initialize embedding model (called lazily from _ensure_embeddings)."""
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
            if not HF_EMBEDDINGS_AVAILABLE:
                logger.warning("⚠️  HuggingFace embeddings not available, using fallback search")
                return

            # Try offline first (model should be pre-cached via `make build`)
            if self._init_hf_embeddings_offline():
                logger.info("🤗 HuggingFace Embeddings initialized (cached)")
                return

            # Model not cached — try online with hard timeout
            logger.warning("⚠️  Model not cached, attempting download (60s timeout)...")
            if self._init_hf_embeddings_online():
                logger.info("🤗 HuggingFace Embeddings initialized (downloaded)")
            else:
                logger.warning("⚠️  Falling back to keyword search")
        else:
            logger.error(f"❌ Unknown embedding model: {model}")

    def _load_or_build_index(self):
        """Load existing index from disk, or prepare documents for deferred build."""
        if self.index_path.exists() and self.metadata_path.exists():
            try:
                self._load_index()
                self._index_built = True
                logger.info(f"📂 Loaded existing FAISS index from {self.index_path}")
            except Exception as e:
                logger.warning(f"Failed to load index: {e}, will rebuild on first search")
                self._prepare_and_defer()
        else:
            self._prepare_and_defer()

    def _prepare_and_defer(self):
        """Prepare documents from source; index building deferred until embeddings ready."""
        self.documents, self.metadata = self._prepare_documents()
        logger.info(f"📋 Prepared {len(self.documents)} documents (index build deferred)")

    def _prepare_documents(self) -> Tuple[List[str], List[Dict[str, Any]]]:
        """Return (doc_texts, metadata) pairs from external source or legacy DB."""
        if self._external_documents:
            docs, metas = [], []
            for doc_text, meta in self._external_documents:
                docs.append(doc_text)
                metas.append(meta)
            return docs, metas

        # Legacy path: build from IsaacAPIDatabase.DATABASE
        docs, metas = [], []
        for func_name, func_info in IsaacAPIDatabase.DATABASE.items():
            doc_text = (
                f"{func_name}: {func_info.get('description', '')}. "
                f"Category: {func_info.get('category', '')}. "
                f"Tags: {', '.join(func_info.get('tags', []))}"
            )
            docs.append(doc_text)
            metas.append({
                "function_name": func_name,
                "description": func_info.get("description", ""),
                "category": func_info.get("category", ""),
                "tags": func_info.get("tags", []),
                "parameters": func_info.get("parameters", []),
                "return_type": func_info.get("return_type", "void"),
                "example_code": func_info.get("example_code", ""),
                "source": "legacy_db",
            })
        return docs, metas

    def _build_index(self):
        """Build FAISS index from prepared documents (caller must ensure embeddings are ready)."""
        self.documents, self.metadata = self._prepare_documents()

        if not self.documents:
            logger.warning("⚠️  No documents to index")
            return

        if not FAISS_AVAILABLE:
            logger.warning("⚠️  FAISS not available, using fallback (metadata populated)")
            return

        if not self.embeddings:
            logger.warning("⚠️  Embeddings not available, using fallback (metadata populated)")
            return

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

        logger.info(f"💾 Saved FAISS index ({len(self.documents)} docs) to {self.index_path}")

    def _load_index(self):
        """Load FAISS index and metadata"""
        if not FAISS_AVAILABLE:
            return

        self.index = faiss.read_index(str(self.index_path))

        with open(self.metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def search(
        self,
        query: str,
        top_k: int = 5,
        metadata_filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant API functions using vector similarity.

        Args:
            query: Natural language query
            top_k: Number of results to return (before filtering)
            metadata_filters: Optional dict of metadata field → value to filter by.
                Supported keys:
                - "dlc_version": str — keep entries compatible with this version
                - "libraries": List[str] — keep entries matching these libraries

        Returns:
            List of matching API references with metadata
        """
        # Lazy-init embeddings on first search
        self._ensure_embeddings()

        if not self.embeddings or not self.index:
            logger.warning("⚠️  Vector search not available, using fallback")
            results = self._fallback_search(query)
        else:
            logger.info(f"🔍 Searching for: {query}")

            # Embed query
            query_embedding = np.array([self.embeddings.embed_query(query)]).astype("float32")

            # Search index — fetch more candidates if we'll be filtering
            fetch_k = top_k * 3 if metadata_filters else top_k
            k = min(fetch_k, len(self.metadata))
            distances, indices = self.index.search(query_embedding, k)

            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx >= 0 and idx < len(self.metadata):
                    meta = dict(self.metadata[idx])
                    meta["score"] = float(distance)
                    results.append(meta)

        # Apply metadata filters
        if metadata_filters:
            results = self._apply_metadata_filters(results, metadata_filters)
            results = results[:top_k]

        logger.info(f"✅ Found {len(results)} matching functions")
        return results

    def _apply_metadata_filters(
        self,
        results: List[Dict[str, Any]],
        filters: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Apply metadata-based filtering to search results.

        Supported filters:
        - dlc_version: str — keep entries where version is compatible
        - libraries: List[str] — keep entries matching library requirements
        """
        filtered = results

        dlc_version = filters.get("dlc_version")
        if dlc_version:
            filtered = [
                r for r in filtered
                if not r.get("versions") or dlc_version in r.get("versions", [])
            ]

        libraries = filters.get("libraries")
        if libraries:
            filtered = [
                r for r in filtered
                if not r.get("libraries") or any(
                    lib in r.get("libraries", []) for lib in libraries
                )
            ]

        return filtered

    def _fallback_search(self, query: str) -> List[Dict[str, Any]]:
        """Fallback keyword-based search over metadata"""
        query_lower = query.lower()
        results = []

        for meta in self.metadata:
            score = 0
            name = meta.get("function_name") or meta.get("function", "")
            desc = meta.get("description", "")
            signature = meta.get("signature", "")

            if query_lower in name.lower():
                score += 10
            if query_lower in desc.lower():
                score += 5
            if query_lower in signature.lower():
                score += 3

            # Check tags if present
            tags = meta.get("tags", [])
            if isinstance(tags, list):
                for tag in tags:
                    if query_lower in str(tag).lower():
                        score += 3

            # Check enhancement summary if present
            enhancement = meta.get("enhancement", {})
            if isinstance(enhancement, dict):
                summary = enhancement.get("summary", "")
                if query_lower in summary.lower():
                    score += 4

            if score > 0:
                result = dict(meta)
                result["score"] = score
                results.append(result)

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:5]

    def get_function_info(self, function_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed info about a specific function from metadata"""
        for meta in self.metadata:
            name = meta.get("function_name") or meta.get("function", "")
            if name == function_name:
                return dict(meta)
        return None

    def list_categories(self) -> List[str]:
        """List all unique categories/groups from metadata"""
        categories = set()
        for meta in self.metadata:
            # Support both 'category' (legacy) and 'class' (KB) as grouping
            cat = meta.get("category") or meta.get("class", "Unknown")
            categories.add(cat)
        return sorted(list(categories))

    def get_apis_by_category(self, category: str) -> List[str]:
        """Get all API function names in a category/class"""
        return [
            meta.get("function_name") or meta.get("function", "")
            for meta in self.metadata
            if (meta.get("category") == category or meta.get("class") == category)
        ]

    def export_database(self) -> Dict[str, Any]:
        """Export all indexed metadata"""
        if self._external_documents:
            return {
                "source": "external",
                "total_entries": len(self.metadata),
                "entries": self.metadata,
            }
        return dict(IsaacAPIDatabase.DATABASE)


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
