"""
Tests for the desktop application components.

These tests focus on logic that doesn't require a running display server.
PyQt widget tests require Xvfb or similar, so we primarily test signals,
data flow, and thread behavior.
"""

import pytest
import sys
from unittest.mock import MagicMock, patch, AsyncMock


class TestAgentThread:
    """Tests for AgentWorker QThread."""

    def test_worker_initialization(self):
        """Worker stores parameters correctly."""
        try:
            from isaac_agent.desktop.agent_thread import AgentWorker
        except ImportError:
            pytest.skip("PyQt6 not available")

        worker = AgentWorker(
            user_input="test mod",
            api_key="sk-test",
            provider="openai",
            model="gpt-4-turbo",
            dlc_version="REP+",
            libraries=["Curlib"],
        )

        assert worker.user_input == "test mod"
        assert worker.api_key == "sk-test"
        assert worker.provider == "openai"
        assert worker.model == "gpt-4-turbo"
        assert worker.dlc_version == "REP+"
        assert worker.libraries == ["Curlib"]

    def test_worker_signals_exist(self):
        """Worker has the expected Qt signals."""
        try:
            from isaac_agent.desktop.agent_thread import AgentWorker
        except ImportError:
            pytest.skip("PyQt6 not available")

        worker = AgentWorker(user_input="test")

        assert hasattr(worker, "stage_changed")
        assert hasattr(worker, "message_added")
        assert hasattr(worker, "code_generated")
        assert hasattr(worker, "xml_generated")
        assert hasattr(worker, "finished")
        assert hasattr(worker, "error_occurred")


class TestTheme:
    """Tests for theme constants."""

    def test_editor_style_has_required_keys(self):
        from isaac_agent.desktop.theme import EDITOR_STYLE

        required = [
            "default", "comment", "keyword", "string", "number",
            "operator", "identifier", "paper", "margin_bg", "caret",
        ]
        for key in required:
            assert key in EDITOR_STYLE, f"Missing style key: {key}"

    def test_app_stylesheet_is_string(self):
        from isaac_agent.desktop.theme import APP_STYLESHEET

        assert isinstance(APP_STYLESHEET, str)
        assert len(APP_STYLESHEET) > 500
        assert "QMainWindow" in APP_STYLESHEET
        assert "QPushButton" in APP_STYLESHEET


class TestWorkflowTimeline:
    """Tests for WorkflowTimeline logic (no PyQt6 needed)."""

    def test_stage_id_map_coverage(self):
        """All known stage names should map to timeline stages."""
        from isaac_agent.desktop._pipeline import PIPELINE_STAGES, STAGE_ID_MAP

        valid_ids = {s["id"] for s in PIPELINE_STAGES}

        # All mapped values should be valid stage IDs or None
        for agent_stage, timeline_stage in STAGE_ID_MAP.items():
            assert timeline_stage is None or timeline_stage in valid_ids, (
                f"Mapped '{agent_stage}' -> '{timeline_stage}' not in {valid_ids}"
            )

    def test_pipeline_stages_ordered(self):
        """Pipeline stages are in the correct order."""
        from isaac_agent.desktop._pipeline import PIPELINE_STAGES

        ids = [s["id"] for s in PIPELINE_STAGES]
        expected = ["parse", "plan", "retrieve", "generate", "validate", "xml_generate", "assemble"]
        assert ids == expected, f"Pipeline order changed: {ids}"

    def test_each_stage_has_label_and_desc(self):
        from isaac_agent.desktop._pipeline import PIPELINE_STAGES

        for stage in PIPELINE_STAGES:
            assert "id" in stage
            assert "label" in stage
            assert "desc" in stage


class TestDesktopPackage:
    """Verify package structure and imports."""

    def test_desktop_package_exists(self):
        """Desktop package is importable (without PyQt)."""
        import isaac_agent.desktop
        assert isaac_agent.desktop.__version__ == "0.1.0"

    def test_theme_importable(self):
        """Theme module is importable."""
        from isaac_agent.desktop.theme import EDITOR_STYLE, APP_STYLESHEET
        assert EDITOR_STYLE
        assert APP_STYLESHEET

    def test_agent_thread_importable(self):
        """Agent thread is importable (requires PyQt to actually run)."""
        try:
            from isaac_agent.desktop.agent_thread import AgentWorker
            assert AgentWorker is not None
        except ImportError as e:
            pytest.skip(f"PyQt6 not available: {e}")


class TestNoApiImport:
    """Verify the old API module is gone."""

    def test_api_module_removed(self):
        """isaac_agent.api should no longer exist."""
        with pytest.raises(ImportError):
            import isaac_agent.api  # noqa: F811

    def test_ui_module_removed(self):
        """isaac_agent.ui should no longer exist."""
        with pytest.raises(ImportError):
            import isaac_agent.ui  # noqa: F811
