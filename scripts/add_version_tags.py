#!/usr/bin/env python3
"""
Backfill script: add DLC version tags, modifiers, and library placeholders
to the existing rag_knowledge_base.json by re-scanning original markdown docs.

Usage:
    python scripts/add_version_tags.py
    python scripts/add_version_tags.py --kb-path processed_docs/rag_knowledge_base.json
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# CSS badge class → compatible DLC versions
BADGE_TO_VERSIONS: Dict[str, List[str]] = {
    "alldlc": ["AB+", "REP", "REP+"],
    "reporplus": ["REP", "REP+"],
    "abrep": ["AB+", "REP"],
    "repplus": ["REP+"],
    "rep": ["REP"],
    "abp": ["AB+"],
}

# CSS classes that are modifiers, not DLC versions
MODIFIER_CLASSES = {"static", "const"}

# All known badge classes
ALL_BADGE_CLASSES = set(BADGE_TO_VERSIONS.keys()) | MODIFIER_CLASSES


def parse_methods_with_badges(content: str) -> List[dict]:
    """Parse a markdown doc content, returning methods in order with badge info.

    Uses the SAME regex pattern as APIDocumentProcessor.extract_class_info()
    to ensure method_id alignment, then separately extracts badge lines by
    looking at the text between each ### and ####.
    """
    content_clean = re.sub(r"^---.*?---\n", "", content, flags=re.DOTALL)

    methods = []
    # Use the EXACT same method-finding pattern as the original processor
    method_pattern = r"### ([^\n]+)\n.*?\n#### (.*?)\n(.*?)(?=^###|$)"
    matches = list(re.finditer(method_pattern, content_clean, re.MULTILINE | re.DOTALL))

    for index, match in enumerate(matches, start=1):
        method_name = match.group(1).strip()
        signature = match.group(2).strip()
        description = match.group(3).strip()

        # Extract badge from the line between ### and ####
        # The match spans from ### to just before the next ### or end
        # The line between ### and #### is matched by .*? — search for badge pattern
        between_text = match.group(0)
        badge_match = re.search(r"\[ ?\]\(#\)\{\: ([^}]*?) \}", between_text)
        badge_classes_str = badge_match.group(1).strip() if badge_match else ""

        badge_classes = _parse_badge_classes(badge_classes_str)
        versions, modifiers = _classify_badge_classes(badge_classes)

        # Clean method name (same as original processor)
        method_name = re.sub(r"·", "", method_name)
        method_name = re.sub(r"\s*\(\)\s*.*", "", method_name)
        method_name = re.sub(r"\s*\{:\s*.*\}\s*$", "", method_name)
        method_name = method_name.strip()

        methods.append({
            "id": f"m{index:03d}",
            "name": method_name,
            "versions": versions,
            "modifiers": modifiers,
        })

    return methods


def _parse_badge_classes(badge_str: str) -> List[str]:
    """Extract individual CSS classes from the badge attribute string.

    Input: '.reporplus .tooltip .badge'
    Output: ['reporplus', 'tooltip', 'badge']
    """
    if not badge_str:
        return []
    classes = []
    for token in badge_str.split():
        token = token.strip().lstrip(".")
        if token:
            classes.append(token)
    # Filter out non-badge classes like 'tooltip', 'badge', 'copyable'
    return [c for c in classes if c in ALL_BADGE_CLASSES]


def _classify_badge_classes(badge_classes: List[str]) -> tuple:
    """Separate badge classes into DLC versions and modifiers."""
    versions: List[str] = []
    modifiers: List[str] = []

    for cls in badge_classes:
        if cls in BADGE_TO_VERSIONS:
            versions.extend(BADGE_TO_VERSIONS[cls])
        elif cls in MODIFIER_CLASSES:
            modifiers.append(cls)

    # Deduplicate while preserving order
    seen = set()
    unique_versions = []
    for v in versions:
        if v not in seen:
            seen.add(v)
            unique_versions.append(v)

    return unique_versions, modifiers


def build_method_map(md_path: Path) -> Dict[str, dict]:
    """Build a mapping from method name + index to badge info for a single markdown file."""
    if not md_path.exists():
        print(f"  ⚠️  Markdown file not found: {md_path}")
        return {}

    content = md_path.read_text(encoding="utf-8")
    methods = parse_methods_with_badges(content)

    return {m["id"]: {"versions": m["versions"], "modifiers": m["modifiers"]} for m in methods}


def backfill_tags(
    kb_path: Path,
    docs_dir: Path,
    dry_run: bool = False,
) -> List[dict]:
    """Main backfill logic: read KB, scan docs, merge tags, return updated entries."""
    if not kb_path.exists():
        print(f"❌ Knowledge base not found: {kb_path}")
        sys.exit(1)

    with open(kb_path, "r", encoding="utf-8") as f:
        entries = json.load(f)

    print(f"📄 Loaded {len(entries)} entries from {kb_path}")

    # Group entries by class
    by_class: Dict[str, list] = {}
    for entry in entries:
        cls = entry.get("class", "Unknown")
        by_class.setdefault(cls, []).append(entry)

    # Build title→path map once (matches processor's title extraction logic)
    title_map = _build_title_map(docs_dir)
    print(f"📁 Indexed {len(title_map)} class titles from markdown files")

    # Cache parsed markdown results (file_stem → method_id → badge info)
    md_cache: Dict[str, Dict[str, dict]] = {}

    updated_count = 0
    missing_count = 0

    for class_name, class_entries in by_class.items():
        md_file = _find_markdown(docs_dir, class_name, title_map)
        if md_file is None:
            print(f"  ⚠️  No markdown found for class '{class_name}', skipping {len(class_entries)} entries")
            missing_count += len(class_entries)
            for entry in class_entries:
                entry.setdefault("versions", [])
                entry.setdefault("modifiers", [])
                entry.setdefault("libraries", [])
            continue

        if md_file.name not in md_cache:
            md_cache[md_file.name] = build_method_map(md_file)

        method_map = md_cache[md_file.name]

        for entry in class_entries:
            method_id = entry.get("method_id", "")
            badge_info = method_map.get(method_id, {})

            entry["versions"] = badge_info.get("versions", [])
            entry["modifiers"] = badge_info.get("modifiers", [])
            entry["libraries"] = []  # reserved for Curlib/RGON

            if entry["versions"]:
                updated_count += 1
            else:
                missing_count += 1

    print(f"\n📊 Results:")
    print(f"   Tagged with versions: {updated_count}")
    print(f"   No version tag found: {missing_count}")

    if dry_run:
        print("\n🔍 Dry run — no changes written.")
    else:
        with open(kb_path, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Updated {kb_path}")

    return entries


def _build_title_map(docs_dir: Path) -> Dict[str, Path]:
    """Scan all markdown files and build a mapping from extracted class title → file path.

    Replicates the title extraction logic from APIDocumentProcessor.extract_class_info():
    1. Try to extract quoted title from '# Class "Title"' or '# Title "Name"' pattern
    2. Fall back to filename (without .md extension)
    """
    title_map: Dict[str, Path] = {}
    for md_file in docs_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        content_clean = re.sub(r"^---.*?---\n", "", content, flags=re.DOTALL)
        title_match = re.search(r'^# .*?"([^"]+)"', content_clean, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        else:
            title = md_file.stem
        title_map[title] = md_file
    return title_map


def _find_markdown(docs_dir: Path, class_name: str, title_map: Optional[Dict[str, Path]] = None) -> Optional[Path]:
    """Find the markdown file for a given class name."""
    if title_map is None:
        title_map = _build_title_map(docs_dir)

    if class_name in title_map:
        return title_map[class_name]

    # Fallback: direct filename match
    direct = docs_dir / f"{class_name}.md"
    if direct.exists():
        return direct

    return None


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Backfill DLC version tags into RAG knowledge base")
    parser.add_argument(
        "--kb-path",
        default=None,
        help="Path to rag_knowledge_base.json (default: auto-detect)",
    )
    parser.add_argument(
        "--docs-dir",
        default=None,
        help="Path to docs/ directory (default: auto-detect)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and report without writing changes",
    )
    args = parser.parse_args()

    # Auto-detect paths relative to this script
    script_dir = Path(__file__).resolve().parent.parent

    kb_path = Path(args.kb_path) if args.kb_path else script_dir / "processed_docs" / "rag_knowledge_base.json"
    docs_dir = Path(args.docs_dir) if args.docs_dir else script_dir / "docs"

    print(f"📁 KB path:  {kb_path}")
    print(f"📁 Docs dir: {docs_dir}")
    print()

    backfill_tags(kb_path, docs_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
