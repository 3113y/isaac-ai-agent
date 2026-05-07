#!/usr/bin/env python3
"""Interactive demo for the Isaac RAG system.

Usage:
    python demo_rag.py                  # Interactive search mode
    python demo_rag.py --stats-only     # Print statistics only
    python demo_rag.py --rebuild        # Force rebuild FAISS index
    python demo_rag.py --legacy         # Use legacy 30-function DB for comparison
"""

import argparse
import sys

from isaac_agent.tools.rag_bridge import RAGBridge, KnowledgeBaseLoader


def main():
    parser = argparse.ArgumentParser(
        description="Isaac AI Agent - RAG System Demo"
    )
    parser.add_argument(
        "--stats-only", action="store_true",
        help="Print statistics and exit"
    )
    parser.add_argument(
        "--rebuild", action="store_true",
        help="Force rebuild FAISS vector index"
    )
    parser.add_argument(
        "--legacy", action="store_true",
        help="Use legacy 30-function database instead of knowledge base"
    )
    parser.add_argument(
        "--kb-path", default=None,
        help="Path to rag_knowledge_base.json (default: auto-detect)"
    )
    parser.add_argument(
        "--top-k", type=int, default=5,
        help="Number of search results to return (default: 5)"
    )
    parser.add_argument(
        "--index-path", default=None,
        help="Path to FAISS index (default: ./data/isaac_api.faiss)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("  Isaac AI Agent - RAG System Demo")
    print("=" * 60)

    bridge = RAGBridge(
        kb_path=args.kb_path,
        use_knowledge_base=not args.legacy,
        index_path=args.index_path,
    )

    if args.rebuild:
        print("\n🔨 Rebuilding FAISS vector index...")
        bridge.rebuild_index()
        print("✅ Index rebuilt successfully")

    # Show statistics
    stats = bridge.get_stats()
    print(f"\n📊 RAG System Statistics:")
    print(f"  Source:            {stats['source']}")
    print(f"  Total entries:     {stats.get('total_entries', 'N/A')}")
    print(f"  Classes:           {stats.get('num_classes', 'N/A')}")
    print(f"  Index size:        {stats['index_size']}")
    print(f"  Embedding model:   {stats['embedding_model']}")
    print(f"  Embeddings ready:  {stats['has_embeddings']}")
    print(f"  Index persisted:   {stats['index_persisted']}")
    print(f"  Index path:        {stats['index_path']}")

    if stats.get("classes"):
        print(f"\n  Classes ({stats['num_classes']}):")
        for cls in stats["classes"][:10]:
            print(f"    - {cls}")
        if stats["num_classes"] > 10:
            print(f"    ... and {stats['num_classes'] - 10} more")

    if args.stats_only:
        return

    # Interactive search loop
    print("\n" + "=" * 60)
    print("  Interactive Search Mode")
    print("  Type your query (or 'quit' to exit, 'stats' for stats)")
    print("=" * 60)

    while True:
        try:
            query = input("\n🔍 Query > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if query.lower() == "stats":
            stats = bridge.get_stats()
            print(f"  Index size: {stats['index_size']} docs")
            print(f"  Embeddings: {'ready' if stats['has_embeddings'] else 'not available'}")
            continue

        # Search
        results = bridge.search(query, top_k=args.top_k)

        print(f"\n  Top {len(results)} results:")
        for i, r in enumerate(results):
            func = r.get("function") or r.get("function_name", "?")
            cls = r.get("class") or r.get("category", "?")
            score = r.get("score", 0)

            enhancement = r.get("enhancement", {})
            if isinstance(enhancement, dict):
                summary = enhancement.get("summary", "N/A")
            else:
                summary = str(enhancement) if enhancement else "N/A"

            print(f"  {i+1}. [{cls}] {func}")
            print(f"     Score: {score:.4f}  |  {summary[:100]}")

        # Show formatted agent context
        print(f"\n{'-' * 40}")
        print("  Formatted Agent Context (what the LLM would receive):")
        print(f"{'-' * 40}")
        context = bridge.get_context_for_agent(query, top_k=args.top_k)
        print(context)


if __name__ == "__main__":
    main()
