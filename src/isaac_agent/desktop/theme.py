"""
Dark theme for the Isaac AI Agent desktop application.

Inspired by Monokai / One Dark Pro — optimized for long coding sessions.
"""

# ── QScintilla Editor Theme ──────────────────────────────────────────────
# Lexer colors (Lua-focused)
EDITOR_STYLE = {
    "default": "#abb2bf",       # Default text
    "comment": "#5c6370",       # -- comments
    "keyword": "#c678dd",       # if, then, end, function, local, return
    "string": "#98c379",        # "strings"
    "number": "#d19a66",        # 123, 3.14
    "operator": "#56b6c2",      # + - * / = == ~=
    "identifier": "#e06c75",    # variable names
    "brace_match": "#528bff",   # matching () {} []
    "margin_bg": "#1e2127",     # Line number gutter
    "margin_fg": "#5c6370",     # Line number text
    "caret": "#528bff",         # Cursor color
    "selection_bg": "#3e4451",  # Selection background
    "paper": "#282c34",         # Editor background
    "fold_margin": "#21252b",   # Code folding gutter
}

# ── Application Stylesheet (Qt CSS) ──────────────────────────────────────
APP_STYLESHEET = """
/* ── Global ─────────────────────────────────── */
QMainWindow {
    background-color: #1e2127;
    color: #abb2bf;
}
QWidget {
    background-color: #1e2127;
    color: #abb2bf;
    font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", "Consolas", monospace;
    font-size: 13px;
}

/* ── Menu Bar ───────────────────────────────── */
QMenuBar {
    background-color: #21252b;
    color: #abb2bf;
    border-bottom: 1px solid #333842;
    padding: 2px;
}
QMenuBar::item {
    padding: 4px 12px;
    background: transparent;
}
QMenuBar::item:selected {
    background-color: #3e4451;
    border-radius: 4px;
}
QMenu {
    background-color: #21252b;
    color: #abb2bf;
    border: 1px solid #333842;
    padding: 4px;
}
QMenu::item {
    padding: 6px 30px 6px 20px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #3e4451;
}
QMenu::separator {
    height: 1px;
    background: #333842;
    margin: 4px 10px;
}

/* ── Tool Bar ───────────────────────────────── */
QToolBar {
    background-color: #21252b;
    border-bottom: 1px solid #333842;
    spacing: 4px;
    padding: 4px;
}
QToolButton {
    background-color: transparent;
    color: #abb2bf;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 4px 12px;
}
QToolButton:hover {
    background-color: #3e4451;
    border-color: #528bff;
}
QToolButton:pressed {
    background-color: #528bff;
    color: #ffffff;
}

/* ── Dock Widgets ───────────────────────────── */
QDockWidget {
    color: #abb2bf;
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
}
QDockWidget::title {
    background-color: #21252b;
    color: #abb2bf;
    padding: 6px 12px;
    border-bottom: 1px solid #333842;
    text-align: left;
}

/* ── Splitter ───────────────────────────────── */
QSplitter::handle {
    background-color: #333842;
    width: 2px;
    height: 2px;
}
QSplitter::handle:hover {
    background-color: #528bff;
}

/* ── Status Bar ─────────────────────────────── */
QStatusBar {
    background-color: #21252b;
    color: #5c6370;
    border-top: 1px solid #333842;
    padding: 2px 8px;
}

/* ── Push Buttons ───────────────────────────── */
QPushButton {
    background-color: #3e4451;
    color: #abb2bf;
    border: 1px solid #333842;
    border-radius: 6px;
    padding: 8px 20px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #4a5161;
    border-color: #528bff;
}
QPushButton:pressed {
    background-color: #528bff;
    color: #ffffff;
}
QPushButton:disabled {
    background-color: #2c313a;
    color: #5c6370;
    border-color: #2c313a;
}
QPushButton#generateButton {
    background-color: #528bff;
    color: #ffffff;
    border-color: #528bff;
    font-size: 14px;
    padding: 10px 30px;
}
QPushButton#generateButton:hover {
    background-color: #61afef;
}
QPushButton#generateButton:disabled {
    background-color: #2c313a;
    color: #5c6370;
    border-color: #2c313a;
}

/* ── Text Area / Input ──────────────────────── */
QTextEdit, QPlainTextEdit {
    background-color: #282c34;
    color: #abb2bf;
    border: 1px solid #333842;
    border-radius: 6px;
    padding: 8px;
    selection-background-color: #3e4451;
}
QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #528bff;
}

/* ── Line Edit ──────────────────────────────── */
QLineEdit {
    background-color: #282c34;
    color: #abb2bf;
    border: 1px solid #333842;
    border-radius: 6px;
    padding: 8px 12px;
    selection-background-color: #3e4451;
}
QLineEdit:focus {
    border-color: #528bff;
}

/* ── Combo Box ──────────────────────────────── */
QComboBox {
    background-color: #282c34;
    color: #abb2bf;
    border: 1px solid #333842;
    border-radius: 6px;
    padding: 6px 12px;
}
QComboBox:hover {
    border-color: #528bff;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox QAbstractItemView {
    background-color: #21252b;
    color: #abb2bf;
    selection-background-color: #3e4451;
    border: 1px solid #333842;
    border-radius: 4px;
    outline: none;
}

/* ── Tab Widget ─────────────────────────────── */
QTabWidget::pane {
    border: 1px solid #333842;
    background-color: #1e2127;
    border-radius: 0;
}
QTabBar::tab {
    background-color: #21252b;
    color: #5c6370;
    border: none;
    padding: 8px 16px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: #282c34;
    color: #abb2bf;
    border-bottom: 2px solid #528bff;
}
QTabBar::tab:hover {
    background-color: #3e4451;
    color: #abb2bf;
}

/* ── Tree View ──────────────────────────────── */
QTreeView {
    background-color: #21252b;
    color: #abb2bf;
    border: none;
    outline: none;
}
QTreeView::item {
    padding: 4px 8px;
    border: none;
}
QTreeView::item:hover {
    background-color: #3e4451;
}
QTreeView::item:selected {
    background-color: #3e4451;
    color: #61afef;
}
QTreeView::branch {
    background-color: #21252b;
}

/* ── Scroll Bars ────────────────────────────── */
QScrollBar:vertical {
    background: #1e2127;
    width: 10px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #3e4451;
    min-height: 30px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #528bff;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar:horizontal {
    background: #1e2127;
    height: 10px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background: #3e4451;
    min-width: 30px;
    border-radius: 5px;
}
QScrollBar::handle:horizontal:hover {
    background: #528bff;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    width: 0;
}

/* ── Group Box ──────────────────────────────── */
QGroupBox {
    border: 1px solid #333842;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
    font-weight: bold;
    color: #abb2bf;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 8px;
}

/* ── Check Box ──────────────────────────────── */
QCheckBox {
    spacing: 8px;
    color: #abb2bf;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 2px solid #5c6370;
    border-radius: 3px;
    background-color: #282c34;
}
QCheckBox::indicator:checked {
    background-color: #528bff;
    border-color: #528bff;
}

/* ── Progress Bar ───────────────────────────── */
QProgressBar {
    background-color: #282c34;
    border: 1px solid #333842;
    border-radius: 4px;
    text-align: center;
    color: #abb2bf;
}
QProgressBar::chunk {
    background-color: #528bff;
    border-radius: 3px;
}

/* ── Label ──────────────────────────────────── */
QLabel#stageLabel {
    font-size: 12px;
    color: #5c6370;
    padding: 2px 8px;
}
QLabel#stageActive {
    font-size: 12px;
    color: #61afef;
    font-weight: bold;
    padding: 2px 8px;
}
QLabel#stageDone {
    font-size: 12px;
    color: #98c379;
    padding: 2px 8px;
}
QLabel#stageError {
    font-size: 12px;
    color: #e06c75;
    font-weight: bold;
    padding: 2px 8px;
}
"""
