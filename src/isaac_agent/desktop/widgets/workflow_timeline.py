"""
Visual workflow timeline widget.

Shows the 7-stage LangGraph pipeline as a series of labeled dots:
    PARSE → PLAN → RETRIEVE → GENERATE → VALIDATE → XML → ASSEMBLE

Each dot lights up as the stage becomes active, turns green on success,
or red on error.
"""

from typing import List, Dict, Optional

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QScrollArea, QFrame,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from isaac_agent.desktop._pipeline import PIPELINE_STAGES, STAGE_ID_MAP


class WorkflowTimeline(QWidget):
    """Horizontal pipeline stage indicator."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stage_widgets: Dict[str, QLabel] = {}
        self._log_labels: List[QLabel] = []
        self._active_index = -1
        self._has_error = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 0)
        layout.setSpacing(4)

        # ── Stage dots row ──────────────────────────────────────────────
        stage_row = QHBoxLayout()
        stage_row.setSpacing(0)

        for i, stage in enumerate(PIPELINE_STAGES):
            if i > 0:
                # Connector arrow
                arrow = QLabel("▸")
                arrow.setObjectName("stageLabel")
                arrow.setStyleSheet("color: #5c6370; padding: 2px 4px; font-size: 10px;")
                arrow.setFixedWidth(16)
                stage_row.addWidget(arrow)

            label = QLabel(stage["label"])
            label.setObjectName("stageLabel")
            label.setToolTip(stage["desc"])
            label.setStyleSheet("color: #5c6370; padding: 2px 6px; font-size: 11px;")
            self._stage_widgets[stage["id"]] = label
            stage_row.addWidget(label)

        stage_row.addStretch()
        layout.addLayout(stage_row)

        # ── Messages/Log area ───────────────────────────────────────────
        self._log_container = QWidget()
        self._log_layout = QVBoxLayout(self._log_container)
        self._log_layout.setContentsMargins(0, 0, 0, 0)
        self._log_layout.setSpacing(1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(60)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll.setWidget(self._log_container)
        layout.addWidget(scroll)

    # ── Public API ──────────────────────────────────────────────────────

    def start(self):
        """Reset all stages to pending state."""
        self._active_index = -1
        self._has_error = False
        for label in self._stage_widgets.values():
            label.setObjectName("stageLabel")
            label.setStyleSheet("color: #5c6370; padding: 2px 6px; font-size: 11px;")

        # Clear logs
        for lbl in self._log_labels:
            self._log_layout.removeWidget(lbl)
            lbl.deleteLater()
        self._log_labels.clear()

        # Show initial log
        self.add_log("system", "Starting workflow...")

    def set_active_stage(self, stage_name: str):
        """Mark a stage as currently active (blue)."""
        stage_id = STAGE_ID_MAP.get(stage_name.lower(), stage_name.lower())
        if stage_id not in self._stage_widgets:
            return

        # Mark all previous stages as done
        for i, stage in enumerate(PIPELINE_STAGES):
            sid = stage["id"]
            label = self._stage_widgets[sid]
            if i < PIPELINE_STAGES.index(
                next(s for s in PIPELINE_STAGES if s["id"] == stage_id)
            ):
                label.setObjectName("stageDone")
                label.setStyleSheet(
                    "color: #98c379; padding: 2px 6px; font-size: 11px; font-weight: bold;"
                )
            elif sid == stage_id:
                label.setObjectName("stageActive")
                label.setStyleSheet(
                    "color: #61afef; padding: 2px 6px; font-size: 11px; font-weight: bold;"
                )
                self._active_index = i

        stage_info = next((s for s in PIPELINE_STAGES if s["id"] == stage_id), None)
        if stage_info:
            self.add_log("agent", f"{stage_info['label']}: {stage_info['desc']}")

    def add_log(self, role: str, text: str):
        """Add a log entry below the timeline."""
        prefix = {"agent": "🤖", "system": "📋", "error": "❌", "user": "👤"}.get(role, "•")
        label = QLabel(f"{prefix} {text[:120]}")
        label.setStyleSheet(
            "color: #5c6370; font-size: 11px; padding: 1px 4px; background: transparent;"
        )
        label.setWordWrap(True)
        self._log_labels.append(label)
        self._log_layout.addWidget(label)

        # Auto-scroll
        self._log_layout.addStretch()

        # Trim if too many
        while len(self._log_labels) > 20:
            old = self._log_labels.pop(0)
            self._log_layout.removeWidget(old)
            old.deleteLater()

    def mark_error(self, error_msg: str):
        """Mark the current stage as errored (red) and show the error."""
        self._has_error = True
        # Mark current active as error
        if 0 <= self._active_index < len(PIPELINE_STAGES):
            sid = PIPELINE_STAGES[self._active_index]["id"]
            label = self._stage_widgets[sid]
            label.setObjectName("stageError")
            label.setStyleSheet(
                "color: #e06c75; padding: 2px 6px; font-size: 11px; font-weight: bold;"
            )
        self.add_log("error", error_msg)

    def mark_complete(self):
        """Mark all stages as done (green)."""
        for label in self._stage_widgets.values():
            label.setObjectName("stageDone")
            label.setStyleSheet(
                "color: #98c379; padding: 2px 6px; font-size: 11px; font-weight: bold;"
            )
        self.add_log("system", "✅ Workflow complete!")

    def reset(self):
        """Reset to initial state."""
        self.start()
