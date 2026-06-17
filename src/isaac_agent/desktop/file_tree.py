"""
File tree panel — browse Isaac mod directory structure.

Uses QTreeView with a custom QFileSystemModel filtered to show
relevant mod files (.lua, .xml, .md).
"""

from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView, QLabel, QHBoxLayout, QPushButton,
    QFileSystemModel,
)
from PyQt6.QtCore import Qt, QDir, pyqtSignal, QModelIndex
from PyQt6.QtGui import QFont

from isaac_agent.config import settings


class FileTreePanel(QWidget):
    """Left panel: mod directory file browser."""

    file_opened = pyqtSignal(str)  # file_path

    def __init__(self, parent=None):
        super().__init__(parent)
        self._root_path: Optional[str] = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # ── Header ──────────────────────────────────────────────────────
        header = QHBoxLayout()
        self._path_label = QLabel("No mod loaded")
        self._path_label.setStyleSheet("color: #5c6370; font-size: 11px; padding: 4px 8px;")
        self._path_label.setWordWrap(True)
        header.addWidget(self._path_label, stretch=1)

        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedSize(28, 28)
        refresh_btn.setToolTip("Refresh file tree")
        refresh_btn.clicked.connect(self.refresh)
        header.addWidget(refresh_btn)

        layout.addLayout(header)

        # ── File tree ───────────────────────────────────────────────────
        self._model = QFileSystemModel()
        self._model.setRootPath("")
        self._model.setNameFilters(["*.lua", "*.xml", "*.md", "*.json", "*.txt"])
        self._model.setNameFilterDisables(False)
        self._model.setFilter(
            QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot
        )

        self._tree = QTreeView()
        self._tree.setModel(self._model)
        self._tree.setRootIndex(self._model.index(""))
        self._tree.setHeaderHidden(True)
        self._tree.setColumnHidden(1, True)  # size
        self._tree.setColumnHidden(2, True)  # type
        self._tree.setColumnHidden(3, True)  # date modified
        self._tree.setAnimated(True)
        self._tree.setIndentation(16)
        self._tree.doubleClicked.connect(self._on_double_click)

        layout.addWidget(self._tree)

    def set_root(self, root_path: str):
        """Set the root directory to display."""
        path = Path(root_path)
        if not path.exists():
            return
        self._root_path = str(path)
        root_index = self._model.index(str(path))
        self._tree.setRootIndex(root_index)
        self._path_label.setText(str(path))
        self._tree.expand(root_index)

    def refresh(self):
        """Refresh the current view."""
        if self._root_path:
            self.set_root(self._root_path)

    def _on_double_click(self, index: QModelIndex):
        """Handle double-click on a file."""
        file_path = self._model.filePath(index)
        path = Path(file_path)
        if path.is_file():
            self.file_opened.emit(file_path)
