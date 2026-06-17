"""
Main window for the Isaac AI Agent desktop application.

VS Code-style layout:
    Left:   File tree (mod directory browser)
    Center: Code editor (QScintilla, tabbed)
    Right:  API browser (RAG search)
    Bottom: Generation panel (prompt + workflow timeline)
"""

import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QDockWidget, QMenuBar, QMenu, QToolBar,
    QStatusBar, QMessageBox, QFileDialog, QApplication, QWidget,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence, QFont

from isaac_agent.desktop.theme import APP_STYLESHEET
from isaac_agent.desktop.editor_panel import EditorPanel
from isaac_agent.desktop.generation_panel import GenerationPanel
from isaac_agent.desktop.settings_dialog import SettingsDialog
from isaac_agent.desktop.agent_thread import AgentWorker
from isaac_agent.desktop.file_tree import FileTreePanel
from isaac_agent.desktop.api_browser import APIBrowserPanel
from isaac_agent.desktop.log_viewer import LogViewerPanel
from isaac_agent.tools.isaac_path_resolver import resolve_all_paths
from isaac_agent.config import settings


class MainWindow(QMainWindow):
    """Top-level application window."""

    def __init__(self):
        super().__init__()
        self._worker: AgentWorker = None
        self._generated_files: dict = {}  # file_path -> lua_code

        self.setWindowTitle("Isaac AI Agent — Mod Code Generator")
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)

        # Apply theme
        self.setStyleSheet(APP_STYLESHEET)

        # Build UI
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_status_bar()
        self._create_panels()

        # Restore window state from settings
        self._restore_state()

        # Auto-detect Isaac paths on startup
        QTimer.singleShot(500, self._detect_isaac_paths)

    # ── Menu Bar ────────────────────────────────────────────────────────

    def _create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction("&New Mod Project", self._new_project, QKeySequence.StandardKey.New)
        file_menu.addAction("&Open Mod...", self._open_mod, QKeySequence.StandardKey.Open)
        file_menu.addSeparator()
        file_menu.addAction("&Save", self._save_current, QKeySequence.StandardKey.Save)
        file_menu.addAction("Save &As...", self._save_as, QKeySequence.StandardKey.SaveAs)
        file_menu.addSeparator()
        file_menu.addAction("E&xit", self.close, QKeySequence.StandardKey.Quit)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.addAction("&Undo", self._undo, QKeySequence.StandardKey.Undo)
        edit_menu.addAction("&Redo", self._redo, QKeySequence.StandardKey.Redo)
        edit_menu.addSeparator()
        edit_menu.addAction("&Find...", self._find, QKeySequence.StandardKey.Find)
        edit_menu.addAction("Find &Next", self._find_next, QKeySequence.StandardKey.FindNext)

        # View menu
        view_menu = menubar.addMenu("&View")
        view_menu.addAction("Toggle &File Tree", self._toggle_file_tree, "Ctrl+1")
        view_menu.addAction("Toggle &API Browser", self._toggle_api_browser, "Ctrl+2")
        view_menu.addAction("Toggle &Log Viewer", self._toggle_log_viewer, "Ctrl+3")

        # Generate menu
        gen_menu = menubar.addMenu("&Generate")
        gen_action = gen_menu.addAction("&Generate Mod", self._trigger_generate)
        gen_action.setShortcut("Ctrl+Return")
        gen_menu.addSeparator()
        gen_menu.addAction("&Build to Mods Folder", self._build_to_mods, "Ctrl+B")

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        tools_menu.addAction("&Settings...", self._show_settings, "Ctrl+,")
        tools_menu.addAction("&Detect Isaac Paths", self._detect_isaac_paths, "Ctrl+D")
        tools_menu.addSeparator()
        tools_menu.addAction("&Analyze Log File...", self._analyze_log, "Ctrl+L")

        # Help menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction("&About...", self._show_about)

    # ── Tool Bar ────────────────────────────────────────────────────────

    def _create_tool_bar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        toolbar.addAction("📁 New", self._new_project)
        toolbar.addAction("📂 Open", self._open_mod)
        toolbar.addAction("💾 Save", self._save_current)
        toolbar.addSeparator()
        toolbar.addAction("⚡ Generate", self._trigger_generate)
        toolbar.addAction("📦 Build", self._build_to_mods)
        toolbar.addSeparator()
        toolbar.addAction("⚙️ Settings", self._show_settings)

    # ── Status Bar ──────────────────────────────────────────────────────

    def _create_status_bar(self):
        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status.showMessage("Ready — Enter a mod description and press Generate (Ctrl+Return)")

    # ── Panels ──────────────────────────────────────────────────────────

    def _create_panels(self):
        # ── Center: Editor ──────────────────────────────────────────────
        self._editor = EditorPanel()
        self.setCentralWidget(self._editor)

        # ── Left dock: File Tree ────────────────────────────────────────
        self._file_tree = FileTreePanel()
        self._file_tree.file_opened.connect(self._editor.open_file)
        self._file_tree_dock = QDockWidget("File Explorer")
        self._file_tree_dock.setWidget(self._file_tree)
        self._file_tree_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
        )
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._file_tree_dock)

        # ── Right dock: API Browser ─────────────────────────────────────
        self._api_browser = APIBrowserPanel()
        self._api_browser_dock = QDockWidget("API Reference")
        self._api_browser_dock.setWidget(self._api_browser)
        self._api_browser_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
        )
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._api_browser_dock)

        # ── Bottom dock: Generation Panel ───────────────────────────────
        self._generation = GenerationPanel()
        self._generation.generate_requested.connect(self._on_generate)
        self._generation_dock = QDockWidget("Mod Generator")
        self._generation_dock.setWidget(self._generation)
        self._generation_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
        )
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._generation_dock)

        # ── Bottom dock: Log Viewer ─────────────────────────────────────
        self._log_viewer = LogViewerPanel()
        self._log_viewer_dock = QDockWidget("Game Log")
        self._log_viewer_dock.setWidget(self._log_viewer)
        self._log_viewer_dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable |
            QDockWidget.DockWidgetFeature.DockWidgetClosable
        )
        # Tabify with generation panel
        self.tabifyDockWidget(self._generation_dock, self._log_viewer_dock)
        self._generation_dock.raise_()  # Show generation panel by default

    # ── Slot: Generate ──────────────────────────────────────────────────

    def _on_generate(self, params: dict):
        """Launch the agent workflow in a background thread."""
        self._generated_files = {}
        self._status.showMessage("Starting workflow...")

        self._worker = AgentWorker(
            user_input=params["user_input"],
            api_key=params.get("api_key"),
            provider=params.get("provider"),
            model=params.get("model"),
            dlc_version=params.get("dlc_version", "REP+"),
            libraries=params.get("libraries"),
        )

        # Connect signals
        self._worker.stage_changed.connect(self._generation.update_stage)
        self._worker.message_added.connect(self._generation.add_message)
        self._worker.code_generated.connect(self._on_code_generated)
        self._worker.xml_generated.connect(self._on_xml_generated)
        self._worker.finished.connect(self._on_workflow_finished)
        self._worker.error_occurred.connect(self._on_workflow_error)

        self._worker.start()

    def _on_code_generated(self, file_path: str, lua_code: str):
        """Handle a generated Lua code file."""
        self._generated_files[file_path] = lua_code
        self._editor.add_generated_code(file_path, lua_code)
        self._status.showMessage(f"Generated: {file_path}")

    def _on_xml_generated(self, xml_file: str, entry_count: int):
        """Handle generated XML content."""
        self._status.showMessage(f"XML generated: {xml_file} ({entry_count} entries)")

    def _on_workflow_finished(self, result):
        """Workflow completed successfully."""
        self._generation.set_generating(False)
        self._generation.timeline.mark_complete()

        file_count = len(getattr(result, "generated_code", []))
        self._status.showMessage(
            f"✅ Generated {file_count} files — Ready to build to mods folder"
        )

        # Refresh file tree if a mod directory is set
        self._file_tree.refresh()

    def _on_workflow_error(self, error_msg: str):
        """Workflow encountered an error."""
        self._generation.mark_error(error_msg)
        self._status.showMessage(f"❌ Error: {error_msg[:100]}")
        QMessageBox.warning(self, "Generation Error", error_msg)

    # ── Menu Actions ────────────────────────────────────────────────────

    def _trigger_generate(self):
        """Programmatic trigger for the generate button."""
        self._generation._on_generate()

    def _new_project(self):
        """Start a new mod project (clear editor)."""
        self._editor.add_generated_code("untitled.lua", "-- New Isaac Mod\nlocal mod = ...\n\n")
        self._generated_files.clear()
        self._status.showMessage("New project started")

    def _open_mod(self):
        """Open an existing mod directory."""
        directory = QFileDialog.getExistingDirectory(
            self, "Open Mod Directory", str(settings.isaac_mod_dir)
        )
        if directory:
            self._file_tree.set_root(directory)
            self._status.showMessage(f"Opened mod: {directory}")

    def _save_current(self):
        """Save current editor tab."""
        editor = self._editor.current_editor
        if editor:
            if editor.file_path:
                editor.save_file()
                self._status.showMessage(f"Saved: {editor.file_path}")
            else:
                self._save_as()

    def _save_as(self):
        """Save current editor tab to a new file."""
        editor = self._editor.current_editor
        if not editor:
            return
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "Lua Files (*.lua);;XML Files (*.xml);;All Files (*)"
        )
        if file_path:
            editor.file_path = file_path
            editor.save_file()
            self._status.showMessage(f"Saved: {file_path}")

    def _undo(self):
        editor = self._editor.current_editor
        if editor:
            editor.undo()

    def _redo(self):
        editor = self._editor.current_editor
        if editor:
            editor.redo()

    def _find(self):
        editor = self._editor.current_editor
        if editor:
            editor.findFirst("", False, False, False, True, True, 0, 0)

    def _find_next(self):
        editor = self._editor.current_editor
        if editor:
            editor.findNext()

    def _build_to_mods(self):
        """Build all generated files into the Isaac mods directory."""
        if not self._generated_files:
            QMessageBox.information(self, "Nothing to Build", "Generate some mod code first.")
            return

        from isaac_agent.build import ModBuilder
        from isaac_agent.core.state import GeneratedCode

        try:
            # Convert to GeneratedCode objects
            code_objects = [
                GeneratedCode(
                    scaffold_type="generated",
                    lua_code=code,
                    file_path=path,
                    role_description="Generated by Isaac AI Agent",
                )
                for path, code in self._generated_files.items()
            ]

            builder = ModBuilder()
            output_dir = builder.build_from_code(code_objects)
            self._status.showMessage(f"✅ Built to: {output_dir}")
            self._file_tree.set_root(str(output_dir))

        except Exception as exc:
            QMessageBox.critical(self, "Build Error", str(exc))

    def _show_settings(self):
        """Open the settings dialog."""
        dialog = SettingsDialog(self)
        if dialog.exec():
            self._status.showMessage("Settings saved — restart may be required for some changes")

    def _detect_isaac_paths(self):
        """Auto-detect Isaac installation paths."""
        try:
            paths = resolve_all_paths()
            if paths.get("mods_dir"):
                self._file_tree.set_root(str(paths["mods_dir"]))
                self._status.showMessage(
                    f"Detected Isaac mods: {paths['mods_dir']}"
                )
                if paths.get("log_file"):
                    self._log_viewer.load_log(str(paths["log_file"]))
            else:
                self._status.showMessage("Isaac paths not found — set manually in Settings")
        except Exception:
            self._status.showMessage("Path detection failed — configure in Settings")

    def _analyze_log(self):
        """Analyze the game log for errors."""
        log_path = getattr(settings, "detected_log_file", "")
        if not log_path or not Path(log_path).exists():
            # Try to detect
            paths = resolve_all_paths()
            log_path = str(paths.get("log_file", ""))

        if log_path and Path(log_path).exists():
            self._log_viewer.load_log(log_path)
            self._log_viewer_dock.raise_()
            self._status.showMessage("Log loaded — check the Game Log panel")
        else:
            QMessageBox.information(
                self, "Log Not Found",
                "Could not find Isaac log.txt.\n"
                "Run the game once to generate a log, or set the path in Settings."
            )

    def _toggle_file_tree(self):
        self._file_tree_dock.setVisible(not self._file_tree_dock.isVisible())

    def _toggle_api_browser(self):
        self._api_browser_dock.setVisible(not self._api_browser_dock.isVisible())

    def _toggle_log_viewer(self):
        self._log_viewer_dock.setVisible(not self._log_viewer_dock.isVisible())

    def _show_about(self):
        QMessageBox.about(
            self, "About Isaac AI Agent",
            "<h2>Isaac AI Agent v0.1.0</h2>"
            "<p>AI-powered mod code generator for<br>"
            "<b>The Binding of Isaac: Repentance</b></p>"
            "<p>Powered by LangGraph + RAG</p>"
            "<hr>"
            "<p>Describe your mod idea in natural language,<br>"
            "and the agent generates complete multi-file Lua mods.</p>"
        )

    # ── State Persistence ───────────────────────────────────────────────

    def _restore_state(self):
        """Restore window geometry from settings."""
        # Minimal: just ensure reasonable defaults
        pass

    def closeEvent(self, event):
        """Handle close event — confirm unsaved changes."""
        # TODO: check for unsaved tabs
        event.accept()
