"""
Tests for RAG Bridge module (KnowledgeBaseLoader + RAGBridge)
"""

import json
import tempfile
from pathlib import Path

import pytest

from isaac_agent.tools.rag_bridge import KnowledgeBaseLoader, RAGBridge
from isaac_agent.tools.vector_rag import VectorRAG, IsaacAPISearchTool, IsaacAPIDatabase


# Sample knowledge base data matching the real rag_knowledge_base.json format
SAMPLE_KB = [
    {
        "class": "EntityPlayer",
        "method_id": "m001",
        "function": "AddHearts",
        "signature": "void EntityPlayer.AddHearts(int count)",
        "description": "Add red heart containers to the player.",
        "enhancement": {
            "summary": "添加红色心之容器给玩家。",
            "use_cases": ["Granting health at level start", "Reward for clearing a room"],
            "key_methods": ["AddHearts", "AddSoulHearts", "GetHearts"],
        },
        "class_enhancement": {
            "summary": "EntityPlayer 表示游戏中的玩家角色，提供生命值、道具、属性等管理功能。",
            "use_cases": ["Player health management", "Item management"],
            "key_methods": ["AddHearts", "GetPlayer", "AddItem"],
        },
    },
    {
        "class": "EntityPlayer",
        "method_id": "m002",
        "function": "AddSoulHearts",
        "signature": "void EntityPlayer.AddSoulHearts(int count)",
        "description": "Add soul heart containers to the player.",
        "enhancement": {
            "summary": "添加灵魂心之容器给玩家。",
            "use_cases": ["Granting soul health", "Spirit heart rewards"],
            "key_methods": ["AddSoulHearts", "AddHearts", "GetSoulHearts"],
        },
        "class_enhancement": {
            "summary": "EntityPlayer 表示游戏中的玩家角色，提供生命值、道具、属性等管理功能。",
            "use_cases": ["Player health management", "Item management"],
            "key_methods": ["AddHearts", "GetPlayer", "AddItem"],
        },
    },
    {
        "class": "Game",
        "method_id": "m003",
        "function": "GetRoom",
        "signature": "Room Game.GetRoom()",
        "description": "Get the current room object.",
        "enhancement": {
            "summary": "获取当前房间对象。",
            "use_cases": ["Accessing room data", "Spawning entities in room"],
            "key_methods": ["GetRoom", "GetLevel", "SpawnExplosion"],
        },
        "class_enhancement": {
            "summary": "Game 是游戏核心管理类，控制关卡、房间、实体生成等功能。",
            "use_cases": ["Level management", "Room navigation"],
            "key_methods": ["GetRoom", "SpawnExplosion", "GetLevel"],
        },
    },
]


@pytest.fixture
def sample_kb_path():
    """Create a temporary knowledge base JSON file."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        json.dump(SAMPLE_KB, f)
    yield f.name
    Path(f.name).unlink(missing_ok=True)


class TestKnowledgeBaseLoader:
    """Test KnowledgeBaseLoader functionality."""

    def test_load(self, sample_kb_path):
        loader = KnowledgeBaseLoader(kb_path=sample_kb_path)
        entries = loader.load()
        assert len(entries) == 3
        assert entries[0]["class"] == "EntityPlayer"

    def test_load_file_not_found(self):
        loader = KnowledgeBaseLoader(kb_path="/nonexistent/path.json")
        with pytest.raises(FileNotFoundError):
            loader.load()

    def test_format_documents(self, sample_kb_path):
        loader = KnowledgeBaseLoader(kb_path=sample_kb_path)
        entries = loader.load()
        docs, metas = loader.format_documents(entries)

        assert len(docs) == 3
        assert len(metas) == 3
        # Check document text contains key fields
        assert "EntityPlayer" in docs[0]
        assert "AddHearts" in docs[0]
        assert "添加红色心之容器给玩家" in docs[0]
        # Check metadata preserves full entry
        assert metas[0]["class"] == "EntityPlayer"
        assert metas[0]["function"] == "AddHearts"
        assert metas[0]["function_name"] == "AddHearts"
        assert metas[0]["source"] == "knowledge_base"
        assert metas[0]["enhancement"]["summary"] == "添加红色心之容器给玩家。"

    def test_get_stats(self, sample_kb_path):
        loader = KnowledgeBaseLoader(kb_path=sample_kb_path)
        entries = loader.load()
        stats = loader.get_stats(entries)

        assert stats["total_entries"] == 3
        assert stats["num_classes"] == 2
        assert "EntityPlayer" in stats["classes"]
        assert "Game" in stats["classes"]

    def test_get_stats_empty(self):
        loader = KnowledgeBaseLoader(kb_path="/nonexistent/path.json")
        stats = loader.get_stats()
        assert stats["total_entries"] == 0


class TestRAGBridge:
    """Test RAGBridge with knowledge base."""

    @pytest.fixture(autouse=True)
    def _setup(self, tmp_path):
        """Use isolated index path to avoid pollution from real FAISS index."""
        self._index_dir = tmp_path / "bridge_test"
        self._index_dir.mkdir()
        self._index_path = str(self._index_dir / "test.faiss")

    def test_init_with_kb(self, sample_kb_path):
        bridge = RAGBridge(
            kb_path=sample_kb_path,
            embedding_model="huggingface",
            use_knowledge_base=True,
            index_path=self._index_path,
        )
        assert bridge is not None
        assert bridge.vector_rag is not None
        assert bridge.use_knowledge_base is True

        # Should have indexed all 3 entries
        if bridge.vector_rag.index:
            assert bridge.vector_rag.index.ntotal == 3

    def test_search(self, sample_kb_path):
        bridge = RAGBridge(
            kb_path=sample_kb_path,
            embedding_model="huggingface",
            use_knowledge_base=True,
            index_path=self._index_path,
        )
        results = bridge.search("player health", top_k=2)
        assert len(results) > 0

        # Should find AddHearts or AddSoulHearts first
        func_names = [r.get("function", "") for r in results]
        assert any("Heart" in name or "health" in str(r).lower() for name, r in zip(func_names, results))

    def test_get_context_for_agent(self, sample_kb_path):
        bridge = RAGBridge(
            kb_path=sample_kb_path,
            embedding_model="huggingface",
            use_knowledge_base=True,
            index_path=self._index_path,
        )
        context = bridge.get_context_for_agent("player health", top_k=2)

        assert "[API Context]" in context
        assert "EntityPlayer" in context
        assert "AddHearts" in context or "AddSoulHearts" in context

    def test_get_stats(self, sample_kb_path):
        bridge = RAGBridge(
            kb_path=sample_kb_path,
            embedding_model="huggingface",
            use_knowledge_base=True,
            index_path=self._index_path,
        )
        stats = bridge.get_stats()

        assert stats["source"] == "knowledge_base"
        assert stats["total_entries"] == 3
        assert stats["num_classes"] == 2

    def test_rebuild_index(self, sample_kb_path):
        bridge = RAGBridge(
            kb_path=sample_kb_path,
            embedding_model="huggingface",
            use_knowledge_base=True,
            index_path=self._index_path,
        )
        bridge.rebuild_index()
        if bridge.vector_rag.index:
            assert bridge.vector_rag.index.ntotal == 3


class TestRAGBridgeLegacyFallback:
    """Test RAGBridge falling back to legacy DB."""

    @pytest.fixture(autouse=True)
    def _setup(self, tmp_path):
        """Use a unique index path per test to avoid pollution from KB tests."""
        self._index_dir = tmp_path / "legacy_test"
        self._index_dir.mkdir()

    def _make_bridge(self):
        return RAGBridge(
            use_knowledge_base=False,
            index_path=str(self._index_dir / "test.faiss"),
        )

    def test_init_legacy_mode(self):
        bridge = self._make_bridge()
        assert bridge.use_knowledge_base is False
        assert bridge.vector_rag is not None

    def test_search_legacy(self):
        bridge = self._make_bridge()
        results = bridge.search("player")
        assert len(results) > 0
        func_names = [r.get("function_name", "") for r in results]
        assert any("Player" in name for name in func_names)

    def test_get_stats_legacy(self):
        bridge = self._make_bridge()
        stats = bridge.get_stats()
        assert stats["source"] == "legacy_db"


class TestBackwardCompat:
    """Test backward compatibility of VectorRAG and IsaacAPISearchTool."""

    def test_vector_rag_without_external_docs(self):
        """VectorRAG should work with legacy DB when no documents provided."""
        rag = VectorRAG(embedding_model="huggingface")
        assert rag is not None

        results = rag.search("player")
        assert len(results) > 0
        assert isinstance(results[0], dict)
        assert "function_name" in results[0]

    def test_vector_rag_with_external_docs(self, sample_kb_path, tmp_path):
        """VectorRAG should accept and index external documents."""
        loader = KnowledgeBaseLoader(kb_path=sample_kb_path)
        entries = loader.load()
        docs, metas = loader.format_documents(entries)

        # Create (text, meta) pairs with isolated index path
        doc_pairs = list(zip(docs, metas))
        index_path = str(tmp_path / "ext_test.faiss")

        rag = VectorRAG(
            embedding_model="huggingface",
            documents=doc_pairs,
            faiss_index_path=index_path,
        )
        assert rag is not None

        # Should index external docs
        if rag.index:
            assert rag.index.ntotal == 3

        results = rag.search("health")
        assert len(results) > 0

    def test_isaac_api_search_tool_wrapper(self):
        """The IsaacAPISearchTool wrapper should still work."""
        tool = IsaacAPISearchTool(use_embeddings=True)
        assert tool is not None
        results = tool.search("player")
        assert len(results) > 0

    def test_isaac_api_database_still_works(self):
        """The legacy database should still be accessible."""
        db = IsaacAPIDatabase.DATABASE
        assert "GetPlayer" in db
        assert "AddHearts" in db
        assert len(db) >= 20
