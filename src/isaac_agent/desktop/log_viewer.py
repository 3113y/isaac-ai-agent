"""
Game log viewer — display and parse Isaac's log.txt for Lua errors.

Bottom panel (tabbed with generation panel) that shows the game log
with error highlighting.
"""

from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton,
    QLabel, QSplitter,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QTextCursor, QSyntaxHighlighter

from isaac_agent.tools.isaac_error_analyzer import parse_log_errors


class LogHighlighter(QSyntaxHighlighter):
    """Highlight Lua errors in log text."""

    def __init__(self, document):
        super().__init__(document)
        self._error_fmt = QTextCharFormat()
        self._error_fmt.setForeground(QColor("#e06c75"))
        self._error_fmt.setFontWeight(700)

        self._warn_fmt = QTextCharFormat()
        self._warn_fmt.setForeground(QColor("#d19a66"))

    def highlightBlock(self, text: str):
        lower = text.lower()
        if any(kw in lower for kw in ["error", "lua err", "traceback", "stack trace"]):
            self.setFormat(0, len(text), self._error_fmt)
        elif any(kw in lower for kw in ["warning", "warn", "deprecated"]):
            self.setFormat(0, len(text), self._warn_fmt)


class LogViewerPanel(QWidget):
    """Bottom panel: Isaac game log viewer."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._log_path: Optional[str] = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # ── Toolbar ─────────────────────────────────────────────────────
        toolbar = QHBoxLayout()

        self._path_label = QLabel("No log loaded")
        self._path_label.setStyleSheet("color: #5c6370; font-size: 11px;")
        toolbar.addWidget(self._path_label, stretch=1)

        reload_btn = QPushButton("🔄 Reload")
        reload_btn.setFixedWidth(80)
        reload_btn.clicked.connect(self.reload)
        toolbar.addWidget(reload_btn)

        analyze_btn = QPushButton("🔍 Analyze")
        analyze_btn.setFixedWidth(100)
        analyze_btn.clicked.connect(self._analyze)
        toolbar.addWidget(analyze_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.setFixedWidth(60)
        clear_btn.clicked.connect(lambda: self._log_view.clear())
        toolbar.addWidget(clear_btn)

        layout.addLayout(toolbar)

        # ── Log text area ───────────────────────────────────────────────
        self._log_view = QTextEdit()
        self._log_view.setReadOnly(True)
        self._log_view.setFont(QFont("Consolas", 10))
        self._log_view.setPlaceholderText(
            "Isaac log.txt will appear here...\n\n"
            "Use Tools → Detect Isaac Paths to find the log, or open it manually."
        )

        # Attach highlighter
        self._highlighter = LogHighlighter(self._log_view.document())

        layout.addWidget(self._log_view)

    def load_log(self, log_path: str):
        """Load and display a log file."""
        path = Path(log_path)
        if not path.exists():
            self._log_view.setPlainText(f"// Log file not found: {log_path}")
            return

        self._log_path = str(path)
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            # Show last 5000 lines for performance
            lines = content.splitlines()
            if len(lines) > 5000:
                shown = lines[-5000:]
                header = f"-- Showing last 5000 of {len(lines)} lines --\n\n"
                self._log_view.setPlainText(header + "\n".join(shown))
            else:
                self._log_view.setPlainText(content)

            # Scroll to end
            cursor = self._log_view.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            self._log_view.setTextCursor(cursor)

            self._path_label.setText(str(path))
        except Exception as exc:
            self._log_view.setPlainText(f"// Failed to read log: {exc}")

    def reload(self):
        """Reload the current log file."""
        if self._log_path:
            self.load_log(self._log_path)

    def _analyze(self):
        """Parse the log for Lua errors and highlight them."""
        if not self._log_path:
            return

        try:
            errors = parse_log_errors(self._log_path)
            if not errors:
                # Insert a note at the top
                self._log_view.insertPlainText("\n\n-- ✅ No Lua errors detected in log --")
                return

            # Highlight errors more prominently
            error_text = "\n\n=== DETECTED LUA ERRORS ===\n"
            for e in errors:
                error_text += (
                    f"\n  [{e.error_type}] {e.message}\n"
                    f"    Line {e.line_number}, file: {e.source}\n"
                )
                if e.stack_trace:
                    error_text += f"    Stack: {e.stack_trace[:120]}...\n"

            self._log_view.append(error_text)

        except Exception as exc:
            self._log_view.append(f"\n\n// Error analysis failed: {exc}")
