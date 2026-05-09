"""
Bridge module connecting the processed knowledge base to VectorRAG.

Provides:
- KnowledgeBaseLoader: reads rag_knowledge_base.json, formats documents for embedding
- RAGBridge: orchestrates loading + VectorRAG search, exposes Agent-friendly interface
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from loguru import logger

from isaac_agent.tools.vector_rag import VectorRAG


class KnowledgeBaseLoader:
    """Loads and formats documents from rag_knowledge_base.json."""

    def __init__(self, kb_path: Optional[str] = None):
        if kb_path is None:
            kb_path = str(
                Path(__file__).resolve().parent.parent.parent.parent
                / "processed_docs"
                / "rag_knowledge_base.json"
            )
        self.kb_path = Path(kb_path)

    def load(self) -> List[Dict[str, Any]]:
        """Load raw entries from the knowledge base JSON."""
        if not self.kb_path.exists():
            raise FileNotFoundError(f"Knowledge base not found at {self.kb_path}")
        with open(self.kb_path, "r", encoding="utf-8") as f:
            entries = json.load(f)
        logger.info(f"📄 Loaded {len(entries)} entries from {self.kb_path}")
        return entries

    def format_documents(
        self, entries: List[Dict[str, Any]]
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        """
        Format knowledge base entries into (doc_texts, metadata) pairs.

        Document text combines semantically significant fields for embedding.
        Metadata preserves full entry info for retrieval result enrichment.
        """
        docs = []
        metas = []

        for entry in entries:
            class_name = entry.get("class", "")
            func_name = entry.get("function", "")
            signature = entry.get("signature", "")
            description = entry.get("description", "")
            enhancement = entry.get("enhancement", {})
            class_enh = entry.get("class_enhancement", {})
            versions = entry.get("versions", [])
            modifiers = entry.get("modifiers", [])
            libraries = entry.get("libraries", [])

            if isinstance(enhancement, dict):
                summary = enhancement.get("summary", "")
                use_cases = enhancement.get("use_cases", [])
            else:
                summary = ""
                use_cases = []

            if isinstance(class_enh, dict):
                class_summary = class_enh.get("summary", "")
            else:
                class_summary = ""

            use_cases_str = "; ".join(use_cases) if use_cases else ""
            versions_str = ", ".join(versions) if versions else "All DLCs"

            # Rich document text for embedding
            doc_text = (
                f"[{class_name}] {func_name} -- {signature}. "
                f"Versions: {versions_str}. "
                f"Summary: {summary}. "
                f"Use cases: {use_cases_str}. "
                f"Class context: {class_summary}. "
                f"Description: {description}"
            )

            docs.append(doc_text)
            metas.append({
                "class": class_name,
                "method_id": entry.get("method_id", ""),
                "function": func_name,
                "function_name": func_name,
                "signature": signature,
                "description": description,
                "versions": versions,
                "modifiers": modifiers,
                "libraries": libraries,
                "enhancement": enhancement,
                "class_enhancement": class_enh,
                "category": class_name,
                "source": "knowledge_base",
            })

        return docs, metas

    def get_stats(self, entries: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Return statistics about the knowledge base."""
        if entries is None:
            try:
                entries = self.load()
            except FileNotFoundError:
                return {"total_entries": 0, "num_classes": 0, "classes": []}

        classes = set()
        for entry in entries:
            classes.add(entry.get("class", "Unknown"))

        return {
            "total_entries": len(entries),
            "num_classes": len(classes),
            "classes": sorted(classes),
            "avg_methods_per_class": round(len(entries) / max(len(classes), 1), 1),
        }


class RAGBridge:
    """
    Bridges the knowledge base to VectorRAG for Agent consumption.

    Loads formatted documents from rag_knowledge_base.json, builds FAISS index,
    and provides search + context-building methods for the LangGraph Agent.
    """

    def __init__(
        self,
        kb_path: Optional[str] = None,
        embedding_model: str = "huggingface",
        index_path: Optional[str] = None,
        use_knowledge_base: bool = True,
        api_key: Optional[str] = None,
    ):
        """
        Initialize the RAG bridge.

        Args:
            kb_path: Path to rag_knowledge_base.json
            embedding_model: "huggingface" or "openai"
            index_path: Path for FAISS index persistence
            use_knowledge_base: If False, falls back to legacy 30-function DB
            api_key: OpenAI API key (only needed for openai embeddings)
        """
        self.use_knowledge_base = use_knowledge_base
        self.loader = KnowledgeBaseLoader(kb_path)

        documents = None
        if use_knowledge_base:
            try:
                entries = self.loader.load()
                _, documents = self.loader.format_documents(entries)
                # Re-format as (text, meta) pairs for VectorRAG
                doc_pairs = self._to_doc_pairs(documents)
                logger.info(f"✅ Loaded {len(doc_pairs)} documents from knowledge base")
            except FileNotFoundError:
                logger.warning("⚠️  Knowledge base not found, falling back to legacy DB")
                doc_pairs = None
        else:
            doc_pairs = None

        self.vector_rag = VectorRAG(
            embedding_model=embedding_model,
            faiss_index_path=index_path,
            api_key=api_key,
            documents=doc_pairs,
        )

        self._documents_meta = documents  # keep for enrichment

    def _to_doc_pairs(
        self, metadata_list: List[Dict[str, Any]]
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """Convert metadata list back to (text, meta) pairs for VectorRAG."""
        pairs = []
        for meta in metadata_list:
            class_name = meta.get("class", "")
            func_name = meta.get("function", "")
            signature = meta.get("signature", "")
            description = meta.get("description", "")
            enhancement = meta.get("enhancement", {})
            class_enh = meta.get("class_enhancement", {})
            versions = meta.get("versions", [])
            modifiers = meta.get("modifiers", [])
            libraries = meta.get("libraries", [])

            if isinstance(enhancement, dict):
                summary = enhancement.get("summary", "")
                use_cases = enhancement.get("use_cases", [])
            else:
                summary = ""
                use_cases = []

            if isinstance(class_enh, dict):
                class_summary = class_enh.get("summary", "")
            else:
                class_summary = ""

            use_cases_str = "; ".join(use_cases) if use_cases else ""
            versions_str = ", ".join(versions) if versions else "All DLCs"

            doc_text = (
                f"[{class_name}] {func_name} -- {signature}. "
                f"Versions: {versions_str}. "
                f"Summary: {summary}. "
                f"Use cases: {use_cases_str}. "
                f"Class context: {class_summary}. "
                f"Description: {description}"
            )
            pairs.append((doc_text, meta))

        return pairs

    def search(
        self,
        query: str,
        top_k: int = 5,
        dlc_version: Optional[str] = None,
        libraries: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Search the knowledge base with optional version/library filtering.

        Args:
            query: Search query string.
            top_k: Number of results to return (before filtering).
            dlc_version: If set, only return APIs compatible with this DLC version
                         (e.g. "REP", "REP+"). An API is compatible if it has no
                         version restriction (empty versions list) or its versions
                         list includes the target version.
            libraries: If set, filter to APIs that require none of these libraries
                       (empty libraries list) or at least one of the listed libraries.
        """
        results = self.vector_rag.search(query, top_k)

        if dlc_version:
            results = [
                r for r in results
                if not r.get("versions") or dlc_version in r.get("versions", [])
            ]

        if libraries:
            entry_libs = set(r.get("libraries", []) for r in results if r.get("libraries"))
            # Include entries with no library requirement (vanilla API)
            # plus entries that use at least one of the requested libraries
            results = [
                r for r in results
                if not r.get("libraries") or any(lib in r.get("libraries", []) for lib in libraries)
            ]

        return results

    def get_context_for_agent(
        self,
        query: str,
        top_k: int = 5,
        dlc_version: Optional[str] = None,
        libraries: Optional[List[str]] = None,
    ) -> str:
        """
        Return formatted text context for LLM prompt injection.

        This is the primary Agent interface: takes a query, returns a
        formatted string the Agent can inject into its prompts.
        """
        results = self.search(query, top_k, dlc_version=dlc_version, libraries=libraries)

        if not results:
            filter_desc = []
            if dlc_version:
                filter_desc.append(f"DLC={dlc_version}")
            if libraries:
                filter_desc.append(f"libraries={libraries}")
            suffix = f" (filtered by {', '.join(filter_desc)})" if filter_desc else ""
            return f"[No API context found for query: {query}{suffix}]"

        lines = ["[API Context]"]
        for i, r in enumerate(results):
            func_name = r.get("function") or r.get("function_name", "Unknown")
            class_name = r.get("class") or r.get("category", "Unknown")
            signature = r.get("signature", "")
            description = r.get("description", "")
            score = r.get("score", 0)
            versions = r.get("versions", [])
            modifiers = r.get("modifiers", [])
            libs = r.get("libraries", [])

            enhancement = r.get("enhancement", {})
            if isinstance(enhancement, dict):
                summary = enhancement.get("summary", "")
                use_cases = enhancement.get("use_cases", [])
            else:
                summary = ""
                use_cases = []

            lines.append(f"\n--- Result {i+1} (score: {score:.4f}) ---")
            lines.append(f"Function: {class_name}.{func_name}")
            if signature:
                lines.append(f"Signature: {signature}")
            # Version badge
            badge_parts = []
            if versions:
                badge_parts.append(f"DLC: {', '.join(versions)}")
            if modifiers:
                badge_parts.append(f"Modifiers: {', '.join(modifiers)}")
            if libs:
                badge_parts.append(f"Libraries: {', '.join(libs)}")
            if badge_parts:
                lines.append(f"Compatibility: {'; '.join(badge_parts)}")
            if summary:
                lines.append(f"Summary: {summary}")
            if description:
                lines.append(f"Description: {description}")
            if use_cases:
                lines.append("Use Cases:")
                for uc in use_cases:
                    lines.append(f"  - {uc}")

        return "\n".join(lines)

    def list_available_versions(self) -> List[str]:
        """List all DLC versions present in the knowledge base."""
        if self.use_knowledge_base:
            try:
                entries = self.loader.load()
                versions = set()
                for e in entries:
                    for v in e.get("versions", []):
                        versions.add(v)
                return sorted(versions)
            except FileNotFoundError:
                pass
        return ["AB+", "REP", "REP+"]  # sensible defaults

    def rebuild_index(self) -> None:
        """Force rebuild the FAISS index from the knowledge base."""
        if not self.use_knowledge_base:
            logger.warning("Knowledge base disabled, rebuilding legacy index")

        self.vector_rag._ensure_embeddings()
        self.vector_rag._build_index()

    def list_categories(self) -> List[str]:
        """List all available API categories from the knowledge base."""
        if self.use_knowledge_base:
            try:
                entries = self.loader.load()
                categories = sorted(set(
                    e.get("class", "Unknown") for e in entries
                ))
                return categories
            except FileNotFoundError:
                pass
        # Fall back to legacy VectorRAG categories
        return self.vector_rag.list_categories()

    def get_stats(self) -> Dict[str, Any]:
        """Return combined statistics."""
        kb_stats = {}
        if self.use_knowledge_base:
            try:
                entries = self.loader.load()
                kb_stats = self.loader.get_stats(entries)
            except FileNotFoundError:
                kb_stats = {"total_entries": 0, "num_classes": 0}

        index_size = self.vector_rag.index.ntotal if self.vector_rag.index else 0
        has_embeddings = self.vector_rag.embeddings is not None
        index_path_exists = self.vector_rag.index_path.exists()

        return {
            **kb_stats,
            "index_size": index_size,
            "has_embeddings": has_embeddings,
            "index_path": str(self.vector_rag.index_path),
            "index_persisted": index_path_exists,
            "embedding_model": self.vector_rag.embedding_model_name,
            "source": "knowledge_base" if self.use_knowledge_base else "legacy_db",
        }
