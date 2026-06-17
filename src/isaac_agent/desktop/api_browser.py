"""
API Browser panel — searchable Isaac API reference from the RAG knowledge base.

Right-side panel that lets users search the Isaac modding API without
leaving the editor.
"""

from typing import Optional, List

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QTextEdit, QListWidget,
    QListWidgetItem, QSplitter,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from isaac_agent.tools.vector_rag import VectorRAG
from isaac_agent.tools.rag_bridge import RAGBridge
from isaac_agent.config import settings


class APIBrowserPanel(QWidget):
    """Right panel: searchable Isaac API documentation."""

    api_selected = pyqtSignal(str, str)  # function_name, signature

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rag: Optional[VectorRAG] = None
        self._bridge: Optional[RAGBridge] = None
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(400)  # debounce
        self._search_timer.timeout.connect(self._do_search)
        self._setup_ui()
        self._init_rag()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Search box
        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Search Isaac API (e.g. \"GetPlayer\")...")
        self._search_input.textChanged.connect(self._on_search_text_changed)
        self._search_input.setClearButtonEnabled(True)
        layout.addWidget(self._search_input)

        # Results list
        self._results_list = QListWidget()
        self._results_list.itemClicked.connect(self._on_result_clicked)
        self._results_list.setAlternatingRowColors(False)
        layout.addWidget(self._results_list)

        # Detail panel
        self._detail = QTextEdit()
        self._detail.setReadOnly(True)
        self._detail.setPlaceholderText("Select an API function to see details...")
        self._detail.setFont(QFont("Consolas", 11))
        layout.addWidget(self._detail)

    def _init_rag(self):
        """Lazy-init the RAG engine."""
        try:
            kb_path = settings.rag_kb_path
            if kb_path and __import__("pathlib").Path(kb_path).exists():
                self._bridge = RAGBridge()
                self._rag = getattr(self._bridge, "rag", None)
        except Exception:
            # Fall back to keyword-only VectorRAG
            try:
                self._rag = VectorRAG()
            except Exception:
                self._rag = None

    def _on_search_text_changed(self, text: str):
        self._search_timer.start()

    def _do_search(self):
        query = self._search_input.text().strip()
        if len(query) < 1:
            self._results_list.clear()
            return

        self._results_list.clear()

        if self._bridge:
            try:
                context = self._bridge.get_context_for_agent(query, top_k=20)
                entries = self._parse_context_to_entries(context)
                for entry in entries:
                    item = QListWidgetItem(entry["label"])
                    item.setData(Qt.ItemDataRole.UserRole, entry)
                    self._results_list.addItem(item)
                return
            except Exception:
                pass

        if self._rag:
            try:
                results = self._rag.search(query, top_k=20)
                for r in results:
                    name = r.get("function", r.get("name", ""))
                    signature = r.get("signature", "")
                    label = f"{name}{signature}" if name else str(r)[:80]
                    item = QListWidgetItem(label)
                    item.setData(Qt.ItemDataRole.UserRole, r)
                    self._results_list.addItem(item)
            except Exception:
                pass

    @staticmethod
    def _parse_context_to_entries(context: str) -> List[dict]:
        """Parse the RAG context string into structured entries."""
        entries = []
        lines = context.split("\n")
        current = {}
        for line in lines:
            line = line.strip()
            if line.startswith("### "):
                if current:
                    entries.append(current)
                current = {"label": line[4:], "description": ""}
            elif current:
                current["description"] += line + "\n"
        if current:
            entries.append(current)
        return entries

    def _on_result_clicked(self, item: QListWidgetItem):
        """Show detail for the selected API function."""
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return

        lines = []
        if isinstance(data, dict):
            name = data.get("label", data.get("function", data.get("name", "")))
            signature = data.get("signature", "")
            desc = data.get("description", data.get("enhancement", ""))

            if name:
                lines.append(f"<h3 style='color:#61afef'>{name}</h3>")
            if signature:
                lines.append(f"<pre style='color:#98c379'>{signature}</pre>")
            if desc:
                desc_str = desc.get("summary", str(desc)) if isinstance(desc, dict) else str(desc)
                lines.append(f"<p style='color:#abb2bf'>{desc_str}</p>")

        self._detail.setHtml("".join(lines))
