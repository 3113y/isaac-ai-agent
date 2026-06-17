"""
Pipeline stage constants — NO PyQt6 dependency.

Separated from workflow_timeline.py so tests can verify stage ordering
and ID mappings without importing PyQt6.
"""

from typing import List, Dict, Optional

# ── Pipeline stage definitions ───────────────────────────────────────────

PIPELINE_STAGES: List[Dict[str, str]] = [
    {"id": "parse",        "label": "📝 Parse",       "desc": "Understanding request"},
    {"id": "plan",         "label": "🏗️ Plan",         "desc": "Designing file structure"},
    {"id": "retrieve",     "label": "🔍 Retrieve",     "desc": "Searching API docs"},
    {"id": "generate",     "label": "⚙️ Generate",     "desc": "Writing Lua code"},
    {"id": "validate",     "label": "✅ Validate",      "desc": "Checking syntax"},
    {"id": "xml_generate", "label": "📄 XML",          "desc": "Generating data files"},
    {"id": "assemble",     "label": "📦 Assemble",     "desc": "Packaging mod"},
]

# Map agent stage IDs to timeline stages
STAGE_ID_MAP: Dict[str, Optional[str]] = {
    "parse": "parse",
    "plan": "plan",
    "retrieve_file": "retrieve",
    "retrieve": "retrieve",
    "generate_file": "generate",
    "generate": "generate",
    "validate": "validate",
    "xml_generate": "xml_generate",
    "assemble": "assemble",
    "complete": "assemble",
    "error": None,
}
