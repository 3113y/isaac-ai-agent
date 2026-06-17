"""
Prompt library — saved mod prompts for quick reuse.

Small dockable panel that stores common or favorite prompts.
"""

import json
from pathlib import Path
from typing import List, Dict

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QHBoxLayout, QPushButton, QInputDialog, QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSignal


PROMPTS_FILE = Path.home() / ".isaac_agent_prompts.json"


class PromptLibraryWidget(QWidget):
    """Saved prompts panel."""

    prompt_selected = pyqtSignal(str)  # prompt text

    def __init__(self, parent=None):
        super().__init__(parent)
        self._prompts: List[Dict[str, str]] = []
        self._load()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # List
        self._list = QListWidget()
        self._list.itemDoubleClicked.connect(self._on_select)
        layout.addWidget(self._list)

        # Buttons
        btn_row = QHBoxLayout()
        save_btn = QPushButton("💾 Save Current")
        save_btn.clicked.connect(self.save_current)
        btn_row.addWidget(save_btn)

        delete_btn = QPushButton("🗑 Delete")
        delete_btn.clicked.connect(self._delete_selected)
        btn_row.addWidget(delete_btn)

        layout.addLayout(btn_row)

        self._refresh_list()

    def _refresh_list(self):
        self._list.clear()
        for entry in self._prompts:
            item = QListWidgetItem(entry.get("name", "Untitled"))
            item.setData(Qt.ItemDataRole.UserRole, entry.get("text", ""))
            self._list.addItem(item)

    def _on_select(self, item: QListWidgetItem):
        text = item.data(Qt.ItemDataRole.UserRole)
        if text:
            self.prompt_selected.emit(text)

    def _delete_selected(self):
        current = self._list.currentRow()
        if 0 <= current < len(self._prompts):
            self._prompts.pop(current)
            self._save()
            self._refresh_list()

    def save_current(self, text: str = ""):
        """Save a prompt to the library."""
        name, ok = QInputDialog.getText(
            self, "Save Prompt", "Prompt name:"
        )
        if ok and name:
            self._prompts.append({"name": name, "text": text})
            self._save()
            self._refresh_list()

    def _load(self):
        """Load prompts from disk."""
        if PROMPTS_FILE.exists():
            try:
                self._prompts = json.loads(PROMPTS_FILE.read_text())
            except Exception:
                self._prompts = []

    def _save(self):
        """Save prompts to disk."""
        PROMPTS_FILE.write_text(json.dumps(self._prompts, indent=2))
