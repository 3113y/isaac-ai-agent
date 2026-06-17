"""
QThread wrapper for running MainAgent without blocking the UI.

The agent's run() is async (LangGraph ainvoke). We run it inside an
asyncio event loop on a background QThread, emitting progress signals.
"""

import asyncio
from typing import Optional, List

from PyQt6.QtCore import QThread, pyqtSignal

from isaac_agent.core.agent import MainAgent
from isaac_agent.core.state import AgentState, WorkflowStage


class AgentWorker(QThread):
    """Runs MainAgent.run() on a background thread with signal-based progress."""

    # ── Signals ──────────────────────────────────────────────────────────
    stage_changed = pyqtSignal(str, str)    # (stage_name, description)
    message_added = pyqtSignal(str, str)     # (role, message_text)
    code_generated = pyqtSignal(str, str)    # (file_path, lua_code)
    xml_generated = pyqtSignal(str, int)     # (xml_file, entry_count)
    finished = pyqtSignal(object)            # AgentState result
    error_occurred = pyqtSignal(str)         # error message

    def __init__(
        self,
        user_input: str,
        api_key: Optional[str] = None,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        dlc_version: str = "REP+",
        libraries: Optional[List[str]] = None,
    ):
        super().__init__()
        self.user_input = user_input
        self.api_key = api_key
        self.provider = provider
        self.model = model
        self.dlc_version = dlc_version
        self.libraries = libraries or []
        self._agent: Optional[MainAgent] = None

    def run(self):
        """Entry point for QThread — runs the async agent workflow."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._execute())
            loop.close()
        except Exception as exc:
            self.error_occurred.emit(str(exc))

    async def _execute(self):
        """Execute the agent workflow and emit progress signals."""
        try:
            self._agent = MainAgent()

            # Run the workflow
            result: AgentState = await self._agent.run(
                user_input=self.user_input,
                api_key=self.api_key,
                provider=self.provider,
                model=self.model,
                dlc_version=self.dlc_version,
                libraries=self.libraries,
            )

            # Emit progress signals from the result
            self._emit_result(result)
            self.finished.emit(result)
            return result

        except Exception as exc:
            self.error_occurred.emit(str(exc))
            raise

    def _emit_result(self, state: AgentState):
        """Walk the final AgentState and emit signals for the UI to consume."""
        # Stage
        stage = state.stage.value if hasattr(state.stage, "value") else str(state.stage)
        self.stage_changed.emit(stage, f"Workflow stage: {stage}")

        # Messages
        for msg in state.messages:
            role = msg.get("role", "system") if isinstance(msg, dict) else "system"
            text = msg.get("content", str(msg)) if isinstance(msg, dict) else str(msg)
            self.message_added.emit(role, text)

        # Generated code files
        for code in state.generated_code:
            file_path = getattr(code, "file_path", "") or "main.lua"
            lua_code = code.lua_code if hasattr(code, "lua_code") else str(code)
            self.code_generated.emit(file_path, lua_code)

        # Generated XML
        for gx in getattr(state, "generated_xml", []):
            xml_file = getattr(gx, "xml_file", "unknown.xml")
            entry_count = len(getattr(gx, "entries", []))
            self.xml_generated.emit(xml_file, entry_count)

        # Error reporting
        for err in state.errors:
            self.message_added.emit("error", err)

    def cancel(self):
        """Request cancellation (best-effort — LangGraph has no native cancel)."""
        if self.isRunning():
            self.terminate()
            self.wait(2000)
