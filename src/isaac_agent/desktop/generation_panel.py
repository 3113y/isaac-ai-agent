"""
Generation panel — prompt input area + Generate button + workflow timeline.

This is the bottom panel of the application where users type their
mod request and trigger the AI agent.
"""

import time
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QComboBox, QLabel, QCheckBox, QFrame, QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal

from isaac_agent.desktop.widgets.workflow_timeline import WorkflowTimeline


class GenerationPanel(QWidget):
    """Bottom panel with prompt input and workflow visualization."""

    generate_requested = pyqtSignal(dict)  # {user_input, provider, model, api_key, dlc, libraries}

    def __init__(self, parent=None):
        super().__init__(parent)
        self._timeline: Optional[WorkflowTimeline] = None
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 4, 8, 8)
        main_layout.setSpacing(6)

        # ── Top row: controls ───────────────────────────────────────────
        controls = QHBoxLayout()
        controls.setSpacing(8)

        # LLM provider
        controls.addWidget(QLabel("Provider:"))
        self._provider_combo = QComboBox()
        self._provider_combo.addItems(["openai", "deepseek", "glm"])
        self._provider_combo.setFixedWidth(100)
        controls.addWidget(self._provider_combo)

        # Model
        controls.addWidget(QLabel("Model:"))
        self._model_combo = QComboBox()
        self._model_combo.setEditable(True)
        self._model_combo.addItems([
            "gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo",
            "deepseek-chat", "deepseek-coder",
            "glm-4", "glm-4-flash",
        ])
        self._model_combo.setFixedWidth(160)
        controls.addWidget(self._model_combo)

        # DLC version
        controls.addWidget(QLabel("DLC:"))
        self._dlc_combo = QComboBox()
        self._dlc_combo.addItems(["REP+", "REP"])
        self._dlc_combo.setFixedWidth(80)
        controls.addWidget(self._dlc_combo)

        # Libraries
        self._curlib_check = QCheckBox("Curlib")
        self._rgon_check = QCheckBox("RGON")
        controls.addWidget(self._curlib_check)
        controls.addWidget(self._rgon_check)

        controls.addStretch()

        # API Key (compact, inside layout)
        controls.addWidget(QLabel("Key:"))
        self._api_key_input = QTextEdit()
        self._api_key_input.setPlaceholderText("API key (optional)")
        self._api_key_input.setFixedHeight(36)
        self._api_key_input.setFixedWidth(180)
        controls.addWidget(self._api_key_input)

        main_layout.addLayout(controls)

        # ── Prompt input bar ────────────────────────────────────────────
        prompt_row = QHBoxLayout()
        prompt_row.setSpacing(8)

        self._prompt_input = QTextEdit()
        self._prompt_input.setPlaceholderText(
            "Describe your mod in natural language...\n"
            "e.g. \"Create a passive item that doubles the player's damage when they're at half a red heart\""
        )
        self._prompt_input.setFixedHeight(72)
        self._prompt_input.setTabChangesFocus(True)
        prompt_row.addWidget(self._prompt_input, stretch=1)

        self._generate_btn = QPushButton("⚡ Generate")
        self._generate_btn.setObjectName("generateButton")
        self._generate_btn.setFixedWidth(140)
        self._generate_btn.setFixedHeight(56)
        self._generate_btn.clicked.connect(self._on_generate)
        self._generate_btn.setShortcut("Ctrl+Return")
        prompt_row.addWidget(self._generate_btn)

        # Cancel button
        self._cancel_btn = QPushButton("Stop")
        self._cancel_btn.setFixedWidth(60)
        self._cancel_btn.setFixedHeight(56)
        self._cancel_btn.setEnabled(False)
        self._cancel_btn.clicked.connect(self._on_cancel)
        prompt_row.addWidget(self._cancel_btn)

        main_layout.addLayout(prompt_row)

        # ── Workflow timeline ───────────────────────────────────────────
        self._timeline = WorkflowTimeline()
        main_layout.addWidget(self._timeline)

    def _on_generate(self):
        """Collect all inputs and emit the generate_requested signal."""
        text = self._prompt_input.toPlainText().strip()
        if not text:
            return

        api_key = self._api_key_input.toPlainText().strip() or None

        # Determine libraries
        libraries = []
        if self._curlib_check.isChecked():
            libraries.append("Curlib")
        if self._rgon_check.isChecked():
            libraries.append("RGON")

        params = {
            "user_input": text,
            "provider": self._provider_combo.currentText(),
            "model": self._model_combo.currentText(),
            "api_key": api_key,
            "dlc_version": self._dlc_combo.currentText(),
            "libraries": libraries if libraries else None,
        }

        self._generate_btn.setEnabled(False)
        self._cancel_btn.setEnabled(True)
        self._timeline.start()
        self.generate_requested.emit(params)

    def _on_cancel(self):
        """Placeholder for cancellation."""
        self.set_generating(False)

    def set_generating(self, active: bool):
        """Toggle UI state during generation."""
        self._generate_btn.setEnabled(not active)
        self._cancel_btn.setEnabled(active)
        self._prompt_input.setReadOnly(active)
        if active:
            self._generate_btn.setText("⏳ Working...")
            self._prompt_input.setStyleSheet("border-color: #528bff;")
        else:
            self._generate_btn.setText("⚡ Generate")
            self._prompt_input.setStyleSheet("")
            self._timeline.reset()

    def update_stage(self, stage_name: str, description: str = ""):
        """Advance the workflow timeline to show current stage."""
        if self._timeline:
            self._timeline.set_active_stage(stage_name)

    def add_message(self, role: str, text: str):
        """Add a log message to the timeline."""
        if self._timeline:
            self._timeline.add_log(role, text)

    def mark_error(self, error_msg: str):
        """Mark the timeline as errored."""
        if self._timeline:
            self._timeline.mark_error(error_msg)
        self.set_generating(False)

    @property
    def timeline(self) -> Optional[WorkflowTimeline]:
        return self._timeline
