"""
Settings dialog — configure LLM provider, API keys, model, and Isaac paths.

Replaces the old .env editing workflow with a proper GUI.
"""

import os
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QPushButton, QTabWidget, QWidget, QFileDialog,
    QSpinBox, QDoubleSpinBox, QGroupBox, QDialogButtonBox,
    QLabel, QMessageBox,
)
from PyQt6.QtCore import Qt

from isaac_agent.config import settings, Settings
from isaac_agent.tools.isaac_path_resolver import resolve_all_paths


class SettingsDialog(QDialog):
    """Application settings dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings — Isaac AI Agent")
        self.setMinimumSize(550, 500)
        self.setModal(True)
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        tabs = QTabWidget()

        # ── LLM Tab ─────────────────────────────────────────────────────
        llm_tab = QWidget()
        llm_layout = QVBoxLayout(llm_tab)

        # Provider group
        prov_group = QGroupBox("LLM Provider")
        prov_form = QFormLayout()
        self._provider_combo = QComboBox()
        self._provider_combo.addItems(["openai", "deepseek", "glm"])
        self._provider_combo.currentTextChanged.connect(self._on_provider_changed)
        prov_form.addRow("Provider:", self._provider_combo)
        prov_group.setLayout(prov_form)
        llm_layout.addWidget(prov_group)

        # OpenAI settings
        self._openai_group = QGroupBox("OpenAI / DeepSeek")
        openai_form = QFormLayout()
        self._openai_key = QLineEdit()
        self._openai_key.setEchoMode(QLineEdit.EchoMode.Password)
        self._openai_key.setPlaceholderText("sk-...")
        openai_form.addRow("API Key:", self._openai_key)
        self._openai_model = QComboBox()
        self._openai_model.setEditable(True)
        self._openai_model.addItems([
            "gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo",
            "deepseek-chat", "deepseek-coder",
        ])
        openai_form.addRow("Model:", self._openai_model)
        self._openai_group.setLayout(openai_form)
        llm_layout.addWidget(self._openai_group)

        # GLM settings
        self._glm_group = QGroupBox("GLM / ZhipuAI")
        glm_form = QFormLayout()
        self._glm_key = QLineEdit()
        self._glm_key.setEchoMode(QLineEdit.EchoMode.Password)
        glm_form.addRow("API Key:", self._glm_key)
        self._glm_model = QComboBox()
        self._glm_model.setEditable(True)
        self._glm_model.addItems(["glm-4", "glm-4-flash"])
        glm_form.addRow("Model:", self._glm_model)
        self._glm_group.setLayout(glm_form)
        llm_layout.addWidget(self._glm_group)

        # Common settings
        common_group = QGroupBox("Generation Settings")
        common_form = QFormLayout()
        self._temperature = QDoubleSpinBox()
        self._temperature.setRange(0.0, 2.0)
        self._temperature.setSingleStep(0.1)
        self._temperature.setValue(0.7)
        common_form.addRow("Temperature:", self._temperature)
        self._max_tokens = QSpinBox()
        self._max_tokens.setRange(256, 32768)
        self._max_tokens.setSingleStep(256)
        self._max_tokens.setValue(4096)
        common_form.addRow("Max Tokens:", self._max_tokens)
        common_group.setLayout(common_form)
        llm_layout.addWidget(common_group)

        llm_layout.addStretch()
        tabs.addTab(llm_tab, "🤖 LLM")

        # ── Paths Tab ───────────────────────────────────────────────────
        paths_tab = QWidget()
        paths_layout = QVBoxLayout(paths_tab)

        paths_group = QGroupBox("Isaac Paths")
        paths_form = QFormLayout()

        self._mods_dir = QLineEdit()
        self._mods_dir.setPlaceholderText("Auto-detected or select manually...")
        mods_browse = QPushButton("Browse...")
        mods_browse.clicked.connect(lambda: self._browse_dir(self._mods_dir, "Select Mods Directory"))
        mods_row = QHBoxLayout()
        mods_row.addWidget(self._mods_dir, stretch=1)
        mods_row.addWidget(mods_browse)
        paths_form.addRow("Mods Dir:", mods_row)

        self._log_file = QLineEdit()
        self._log_file.setPlaceholderText("Auto-detected or select manually...")
        log_browse = QPushButton("Browse...")
        log_browse.clicked.connect(lambda: self._browse_file(self._log_file, "Select log.txt", "Text Files (*.txt)"))
        log_row = QHBoxLayout()
        log_row.addWidget(self._log_file, stretch=1)
        log_row.addWidget(log_browse)
        paths_form.addRow("Log File:", log_row)

        paths_group.setLayout(paths_form)
        paths_layout.addWidget(paths_group)

        detect_btn = QPushButton("🔍 Auto-Detect Paths")
        detect_btn.clicked.connect(self._auto_detect)
        paths_layout.addWidget(detect_btn)

        paths_layout.addStretch()
        tabs.addTab(paths_tab, "📁 Paths")

        # ── Data Tab ────────────────────────────────────────────────────
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)

        data_group = QGroupBox("RAG & Data")
        data_form = QFormLayout()
        self._rag_path = QLineEdit()
        self._rag_path.setPlaceholderText("./processed_docs/rag_knowledge_base.json")
        data_form.addRow("RAG KB:", self._rag_path)
        self._faiss_path = QLineEdit()
        self._faiss_path.setPlaceholderText("./data/isaac_api.faiss")
        data_form.addRow("FAISS Index:", self._faiss_path)
        self._xml_cache = QLineEdit()
        self._xml_cache.setPlaceholderText("./data/xml_schemas_cache.json")
        data_form.addRow("XML Cache:", self._xml_cache)
        data_group.setLayout(data_form)
        data_layout.addWidget(data_group)

        data_layout.addStretch()
        tabs.addTab(data_tab, "💾 Data")

        layout.addWidget(tabs)

        # ── Dialog Buttons ──────────────────────────────────────────────
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Apply
        )
        buttons.accepted.connect(self._save_and_accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self._save_settings)
        layout.addWidget(buttons)

    def _load_settings(self):
        """Populate fields from current settings."""
        self._provider_combo.setCurrentText(settings.llm_provider)
        self._openai_key.setText(settings.openai_api_key or "")
        self._openai_model.setCurrentText(settings.openai_model)
        self._glm_key.setText(settings.glm_api_key or "")
        self._glm_model.setCurrentText(settings.glm_model)
        self._temperature.setValue(settings.temperature)
        self._max_tokens.setValue(settings.max_tokens)
        self._mods_dir.setText(settings.isaac_mod_dir or "")
        self._log_file.setText(settings.detected_log_file or "")
        self._rag_path.setText(settings.rag_kb_path)
        self._faiss_path.setText(settings.faiss_index_path)
        self._xml_cache.setText(settings.xml_schema_cache_path)
        self._on_provider_changed(self._provider_combo.currentText())

    def _on_provider_changed(self, provider: str):
        """Show/hide groups based on selected provider."""
        is_openai = provider in ("openai", "deepseek")
        self._openai_group.setVisible(is_openai)
        self._glm_group.setVisible(provider == "glm")

    def _auto_detect(self):
        """Auto-detect Isaac paths and update fields."""
        try:
            paths = resolve_all_paths()
            if paths.get("mods_dir"):
                self._mods_dir.setText(str(paths["mods_dir"]))
            if paths.get("log_file"):
                self._log_file.setText(str(paths["log_file"]))
            QMessageBox.information(self, "Detection Complete", f"Found:\nMods: {paths.get('mods_dir')}\nLog: {paths.get('log_file')}")
        except Exception as exc:
            QMessageBox.warning(self, "Detection Failed", str(exc))

    def _browse_dir(self, target: QLineEdit, title: str):
        path = QFileDialog.getExistingDirectory(self, title, target.text() or os.path.expanduser("~"))
        if path:
            target.setText(path)

    def _browse_file(self, target: QLineEdit, title: str, filter_str: str):
        path, _ = QFileDialog.getOpenFileName(self, title, target.text() or os.path.expanduser("~"), filter_str)
        if path:
            target.setText(path)

    def _save_settings(self):
        """Write settings to .env file."""
        env_path = Path(".env")
        env_lines = {}

        # Read existing .env
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, _, val = line.partition("=")
                    env_lines[key.strip()] = val.strip().strip('"')

        # Update with current values
        updates = {
            "LLM_PROVIDER": self._provider_combo.currentText(),
            "OPENAI_API_KEY": self._openai_key.text() or "",
            "OPENAI_MODEL": self._openai_model.currentText(),
            "GLM_API_KEY": self._glm_key.text() or "",
            "GLM_MODEL": self._glm_model.currentText(),
            "LLM_TEMPERATURE": str(self._temperature.value()),
            "LLM_MAX_TOKENS": str(self._max_tokens.value()),
            "ISAAC_MOD_DIR": self._mods_dir.text() or "./mods",
            "RAG_KB_PATH": self._rag_path.text() or "",
            "FAISS_INDEX_PATH": self._faiss_path.text() or "",
            "XML_SCHEMA_CACHE_PATH": self._xml_cache.text() or "",
        }
        env_lines.update(updates)

        # Write .env
        content = "\n".join(f'{k}="{v}"' for k, v in env_lines.items() if v)
        env_path.write_text(content + "\n")

        # Reload settings (in-process)
        for key, value in updates.items():
            field_name = key.lower()
            if hasattr(settings, field_name):
                setattr(settings, field_name, value)

    def _save_and_accept(self):
        self._save_settings()
        self.accept()
