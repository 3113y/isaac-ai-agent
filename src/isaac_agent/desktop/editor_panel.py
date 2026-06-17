"""
QScintilla-based Lua code editor panel.

Provides syntax highlighting, line numbers, code folding, auto-indent,
and a Monokai-inspired color scheme.
"""

from pathlib import Path

from PyQt6.Qsci import QsciScintilla, QsciLexerLua
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import pyqtSignal

from isaac_agent.desktop.theme import EDITOR_STYLE


# ── Lua Lexer with custom Monokai colors ─────────────────────────────────

class MonokaiLuaLexer(QsciLexerLua):
    """Lua lexer with Monokai-inspired syntax coloring."""

    def __init__(self, parent=None):
        super().__init__(parent)

        bg = QColor(EDITOR_STYLE["paper"])
        default_fg = QColor(EDITOR_STYLE["default"])

        # Default
        self.setDefaultColor(default_fg)
        self.setDefaultPaper(bg)
        self.setDefaultFont(self._editor_font())

        # Lua-specific styles
        self.setColor(QColor(EDITOR_STYLE["default"]), QsciLexerLua.Default)
        self.setColor(QColor(EDITOR_STYLE["comment"]), QsciLexerLua.Comment)
        self.setColor(QColor(EDITOR_STYLE["comment"]), QsciLexerLua.LineComment)
        self.setColor(QColor(EDITOR_STYLE["number"]), QsciLexerLua.Number)
        self.setColor(QColor(EDITOR_STYLE["keyword"]), QsciLexerLua.Keyword)
        self.setColor(QColor(EDITOR_STYLE["string"]), QsciLexerLua.String)
        self.setColor(QColor(EDITOR_STYLE["string"]), QsciLexerLua.Character)
        self.setColor(QColor(EDITOR_STYLE["string"]), QsciLexerLua.LiteralString)
        self.setColor(QColor(EDITOR_STYLE["operator"]), QsciLexerLua.Operator)
        self.setColor(QColor(EDITOR_STYLE["identifier"]), QsciLexerLua.Identifier)

        # Paper colors
        self.setPaper(bg, QsciLexerLua.Default)
        self.setPaper(bg, QsciLexerLua.Comment)
        self.setPaper(bg, QsciLexerLua.Number)
        self.setPaper(bg, QsciLexerLua.Keyword)
        self.setPaper(bg, QsciLexerLua.String)
        self.setPaper(bg, QsciLexerLua.Operator)
        self.setPaper(bg, QsciLexerLua.Identifier)

        # Font for each style
        for style in range(QsciLexerLua.Operator + 1):
            self.setFont(self._editor_font(), style)

    @staticmethod
    def _editor_font() -> QFont:
        font = QFont("Cascadia Code", 12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        return font


# ── Single Code Editor Tab ──────────────────────────────────────────────

class CodeEditor(QsciScintilla):
    """A single QScintilla editor configured for Lua."""

    file_saved = pyqtSignal(str)  # file_path

    def __init__(self, parent=None):
        super().__init__(parent)
        self._file_path: str = ""
        self._modified = False

        # Lexer
        self._lexer = MonokaiLuaLexer(self)
        self.setLexer(self._lexer)

        # ── Appearance ──────────────────────────────────────────────────
        self.setUtf8(True)

        # Line numbers
        self.setMarginsBackgroundColor(QColor(EDITOR_STYLE["margin_bg"]))
        self.setMarginsForegroundColor(QColor(EDITOR_STYLE["margin_fg"]))
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "0000")
        self.setMarginLineNumbers(0, True)

        # Code folding
        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle)
        self.setFoldMarginColors(
            QColor(EDITOR_STYLE["fold_margin"]),
            QColor(EDITOR_STYLE["fold_margin"]),
        )

        # Caret
        self.setCaretForegroundColor(QColor(EDITOR_STYLE["caret"]))
        self.setCaretWidth(2)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#2c313a"))

        # Selection
        self.setSelectionBackgroundColor(QColor(EDITOR_STYLE["selection_bg"]))

        # ── Behavior ────────────────────────────────────────────────────
        self.setAutoIndent(True)
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setBackspaceUnindents(True)
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)

        # Edge line at 120 chars
        self.setEdgeMode(QsciScintilla.EdgeMode.EdgeLine)
        self.setEdgeColumn(120)
        self.setEdgeColor(QColor("#333842"))

        # ── Scrollbar ───────────────────────────────────────────────────
        self.setScrollWidth(1)
        self.setScrollWidthTracking(True)

        # ── Signals ─────────────────────────────────────────────────────
        self.modificationChanged.connect(self._on_modified)

    @property
    def file_path(self) -> str:
        return self._file_path

    @file_path.setter
    def file_path(self, path: str):
        self._file_path = path

    @property
    def is_modified(self) -> bool:
        return self._modified

    def load_file(self, file_path: str):
        """Load a file from disk into the editor."""
        path = Path(file_path)
        if not path.exists():
            return
        self.setText(path.read_text(encoding="utf-8", errors="replace"))
        self._file_path = str(path)
        self._modified = False
        self.setModified(False)

    def save_file(self):
        """Save editor content to disk."""
        if self._file_path:
            Path(self._file_path).write_text(self.text(), encoding="utf-8")
            self._modified = False
            self.setModified(False)
            self.file_saved.emit(self._file_path)

    def set_lua_content(self, content: str, file_path: str = ""):
        """Set editor content programmatically (e.g., generated code)."""
        self.setText(content)
        self._file_path = file_path
        self._modified = True
        self.setModified(True)

    def _on_modified(self, modified: bool):
        self._modified = modified


# ── Editor Panel (tab widget of editors) ─────────────────────────────────

class EditorPanel(QWidget):
    """Multi-tab code editor panel."""

    tab_closed = pyqtSignal(str)  # file_path

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tabs = QTabWidget()
        self._tabs.setTabsClosable(True)
        self._tabs.setMovable(True)
        self._tabs.tabCloseRequested.connect(self._close_tab)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._tabs)

        # Start with an empty editor
        self._new_tab("untitled.lua", "-- Isaac AI Agent\n-- Generated mod code\n\n")

    @property
    def current_editor(self) -> CodeEditor:
        widget = self._tabs.currentWidget()
        if isinstance(widget, CodeEditor):
            return widget
        return self._editors()[0] if self._editors() else None

    def _editors(self):
        return [
            self._tabs.widget(i)
            for i in range(self._tabs.count())
            if isinstance(self._tabs.widget(i), CodeEditor)
        ]

    def _new_tab(self, title: str, content: str = "") -> CodeEditor:
        editor = CodeEditor()
        editor.set_lua_content(content, title)
        self._tabs.addTab(editor, title)
        self._tabs.setCurrentWidget(editor)
        return editor

    def _close_tab(self, index: int):
        if self._tabs.count() <= 1:
            return  # keep at least one tab
        widget = self._tabs.widget(index)
        self._tabs.removeTab(index)
        if isinstance(widget, CodeEditor):
            self.tab_closed.emit(widget.file_path)

    def open_file(self, file_path: str):
        """Open a file in a new or existing tab."""
        name = Path(file_path).name
        # Check if already open
        for editor in self._editors():
            if editor.file_path == file_path:
                self._tabs.setCurrentWidget(editor)
                return
        editor = self._new_tab(name)
        editor.load_file(file_path)

    def add_generated_code(self, file_path: str, lua_code: str):
        """Add a generated code file as a new tab."""
        name = Path(file_path).name if file_path else "generated.lua"
        editor = self._new_tab(name, lua_code)
        editor.file_path = file_path
        editor.setModified(True)

    def add_xml_content(self, file_name: str, xml_content: str):
        """Add generated XML content as a new tab."""
        name = Path(file_name).name if file_name else "generated.xml"
        editor = self._new_tab(name, xml_content)
        editor.file_path = file_name
        editor.setModified(True)
