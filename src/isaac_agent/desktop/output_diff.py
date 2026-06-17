"""
Output diff viewer — side-by-side comparison of generated vs existing code.

Optional panel for reviewing changes before writing to the mod folder.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QSyntaxHighlighter


class DiffHighlighter(QSyntaxHighlighter):
    """Highlight diff output: green for additions, red for deletions."""

    def __init__(self, document):
        super().__init__(document)
        self._add_fmt = QTextCharFormat()
        self._add_fmt.setForeground(QColor("#98c379"))
        self._add_fmt.setBackground(QColor("#1a3a1a"))

        self._del_fmt = QTextCharFormat()
        self._del_fmt.setForeground(QColor("#e06c75"))
        self._del_fmt.setBackground(QColor("#3a1a1a"))

        self._hdr_fmt = QTextCharFormat()
        self._hdr_fmt.setForeground(QColor("#61afef"))
        self._hdr_fmt.setFontWeight(700)

    def highlightBlock(self, text: str):
        if text.startswith("+"):
            self.setFormat(0, len(text), self._add_fmt)
        elif text.startswith("-"):
            self.setFormat(0, len(text), self._del_fmt)
        elif text.startswith("@@"):
            self.setFormat(0, len(text), self._hdr_fmt)


class OutputDiffPanel(QWidget):
    """Side-by-side diff view for comparing code versions."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Headers
        headers = QHBoxLayout()
        left_hdr = QLabel("Original")
        left_hdr.setStyleSheet("color: #e06c75; font-weight: bold; padding: 4px 8px;")
        right_hdr = QLabel("Generated")
        right_hdr.setStyleSheet("color: #98c379; font-weight: bold; padding: 4px 8px;")
        headers.addWidget(left_hdr, stretch=1)
        headers.addWidget(right_hdr, stretch=1)
        layout.addLayout(headers)

        # Editors
        editors = QHBoxLayout()
        self._left = QTextEdit()
        self._left.setReadOnly(True)
        self._left.setFont(QFont("Consolas", 11))
        editors.addWidget(self._left, stretch=1)

        self._right = QTextEdit()
        self._right.setReadOnly(True)
        self._right.setFont(QFont("Consolas", 11))
        editors.addWidget(self._right, stretch=1)

        layout.addLayout(editors, stretch=1)

    def show_diff(self, original: str, generated: str):
        """Display original vs generated code side by side."""
        self._left.setPlainText(original)
        self._right.setPlainText(generated)

    def clear(self):
        self._left.clear()
        self._right.clear()
