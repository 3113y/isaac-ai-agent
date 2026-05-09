"""
Isaac AI Agent — NiceGUI web-based graphical interface.

Usage:
    python -m isaac_agent.ui.app
    # or: make ui
    # Open http://localhost:8080 in any browser.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

from loguru import logger
from nicegui import app, ui

from isaac_agent.core.state import WorkflowStage

# Default models per provider (auto-filled when provider changes)
PROVIDER_MODELS = {
    "openai": "gpt-4-turbo",
    "glm": "glm-4",
    "deepseek": "deepseek-chat",
}

# ---------------------------------------------------------------------------
# Global agent instance (MainAgent imported lazily to keep server startup fast)
# ---------------------------------------------------------------------------

_agent: Any = None
_agent_ready = False

# ---------------------------------------------------------------------------
# Workflow stage helpers
# ---------------------------------------------------------------------------

STAGE_ORDER = [
    WorkflowStage.PARSE,
    WorkflowStage.RETRIEVE,
    WorkflowStage.GENERATE,
    WorkflowStage.VALIDATE,
    WorkflowStage.COMPLETE,
]

STAGE_META = {
    WorkflowStage.PARSE:    ("📝", "解析"),
    WorkflowStage.RETRIEVE: ("🔍", "检索"),
    WorkflowStage.GENERATE: ("⚙️", "生成"),
    WorkflowStage.VALIDATE: ("✔️", "验证"),
    WorkflowStage.COMPLETE: ("🎉", "完成"),
    WorkflowStage.ERROR:    ("❌", "错误"),
}


def _stage_html(stage: WorkflowStage, status: str) -> str:
    colors = {
        "pending": ("#555", "#888"),
        "active":  ("#3b82f6", "#e0e0e0"),
        "done":    ("#22c55e", "#22c55e"),
        "error":   ("#ef4444", "#ef4444"),
    }
    dot, text = colors.get(status, colors["pending"])
    icon, label = STAGE_META.get(stage, ("", stage.value))
    weight = "font-weight:bold;" if status == "active" else ""
    return (
        f'<div style="display:flex;align-items:center;gap:10px;margin:4px 0;">'
        f'<div style="width:12px;height:12px;border-radius:50%;background:{dot};'
        f'flex-shrink:0;"></div>'
        f'<span style="color:{text};{weight}">{icon} {label}</span>'
        f'</div>'
    )


def _all_stages_html(current_stage: WorkflowStage | None) -> str:
    if current_stage is None:
        return "".join(_stage_html(s, "pending") for s in STAGE_ORDER)
    parts = []
    reached = False
    for s in STAGE_ORDER:
        if s == current_stage:
            status = "done" if s != WorkflowStage.ERROR else "error"
            reached = True
        elif not reached:
            status = "done"
        else:
            status = "pending"
        parts.append(_stage_html(s, status))
    return "".join(parts)


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------

@app.on_startup
async def init_agent():
    global _agent, _agent_ready
    print("Starting agent initialization in background...", flush=True)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, _init_agent_sync)


def _init_agent_sync():
    global _agent, _agent_ready
    try:
        from isaac_agent.core.agent import MainAgent  # heavy import — done in background
        print("Initializing Isaac AI Agent (loading models + FAISS index)...", flush=True)
        _agent = MainAgent()
        _agent_ready = True
        print("Agent ready.", flush=True)
    except Exception as e:
        print(f"Agent init failed: {e}", flush=True)
        import traceback
        traceback.print_exc()


# ---------------------------------------------------------------------------
# Health check (no JS needed)
# ---------------------------------------------------------------------------

@ui.page("/ping")
def ping():
    ui.label("✅ Isaac AI Agent 服务器正在运行。")
    ui.label(f"智能体就绪: {_agent_ready}")


@ui.page("/test")
def test_page():
    """Zero-JS diagnostic page — confirms basic HTTP connectivity."""
    ui.add_body_html("""
    <div style="padding:2em;font-family:sans-serif;color:#e0e0e0;background:#1a1a1a;min-height:100vh;">
      <h1>连接测试</h1>
      <p style="color:#22c55e;font-size:1.2em;">如果你能看到这段文字，说明 HTTP 连接正常。</p>
      <p>此页面不需要 JavaScript 或 WebSocket。</p>
      <hr>
      <p>现在测试<a href="/" style="color:#3b82f6;">主页面 →</a>（需要 WebSocket）</p>
      <p>或查看<a href="/ping" style="color:#3b82f6;">服务器状态 →</a></p>
    </div>
    """)


# ---------------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------------

@ui.page("/")
def main_page() -> None:
    ui.add_body_html("""
    <noscript>
      <div style="padding:2em;font-family:sans-serif;color:#e0e0e0;background:#1a1a1a;min-height:100vh;">
        <h1>🎮 Isaac AI Agent</h1>
        <p style="color:#ef4444;"><b>JavaScript 已禁用或加载失败。</b></p>
        <p>此应用需要启用 JavaScript 的现代浏览器。</p>
        <p>如果你在现代浏览器中看到此提示，可能是 WebSocket 连接被阻止。</p>
        <p>请检查浏览器是否能访问 8080 端口。</p>
        <hr>
        <p><a href="/ping" style="color:#3b82f6;">→ 服务器健康检查</a></p>
      </div>
    </noscript>
    """)
    ui.dark_mode().enable()

    # Mutable refs for elements that the agent-ready timer needs to update
    _refs: dict = {}

    # ---- Header ----
    with ui.header(elevated=True).classes("items-center justify-between"):
        ui.label("🎮 Isaac AI Agent — TBOI Mod 代码生成器").classes("text-xl font-bold")
        _refs["ready_badge"] = ui.badge("智能体就绪", color="green")
        _refs["ready_badge"].set_visibility(_agent_ready)
        _refs["loading_badge"] = ui.badge("正在初始化...", color="orange")
        _refs["loading_badge"].set_visibility(not _agent_ready)

    with ui.row().classes("w-full q-px-md q-pb-md gap-4"):
        # ============================================== LEFT COLUMN
        with ui.column().classes("w-2/5 gap-4"):
            # -- Mod Request --
            with ui.card().classes("w-full"):
                ui.label("Mod 请求").classes("text-lg font-bold")
                prompt_textarea = (
                    ui.textarea(
                        placeholder='例如："创建一个拾取时恢复 2 颗红心的新道具..."'
                    )
                    .classes("w-full")
                    .props("rows=4")
                )

                with ui.row().classes("gap-4 items-end"):
                    provider_select = (
                        ui.select(
                            options=["openai", "glm", "deepseek"],
                            value="openai",
                            label="LLM 提供商",
                        )
                        .classes("w-32")
                    )
                    model_input = ui.input(value="gpt-4-turbo", label="模型").classes("w-36")

                # Auto-fill model name when provider changes
                def _on_provider_change(e):
                    new_model = PROVIDER_MODELS.get(e.value, "gpt-4-turbo")
                    model_input.set_value(new_model)

                provider_select.on("update:model-value", _on_provider_change)

                api_key_input = (
                    ui.input(
                        value="",
                        label="API 密钥",
                        password=True,
                        placeholder="输入你的 API 密钥（不会保存到服务器）...",
                    )
                    .classes("w-full")
                    .props("autocomplete=off")
                )

                # DLC Version and Library selectors
                with ui.row().classes("gap-4 items-center mt-2"):
                    dlc_select = (
                        ui.select(
                            options=["REP+", "REP"],
                            value="REP+",
                            label="DLC 版本",
                        )
                        .classes("w-24")
                    )
                    ui.label("前置库:").classes("text-sm text-gray-400")
                    curlib_check = ui.checkbox("Curlib", value=False)
                    rgon_check = ui.checkbox("RGON", value=False)
                    ui.label("(文档尚未接入)").classes("text-xs text-gray-500")

                # Auto-detected path status
                _refs["path_status"] = ui.html("")

                def _update_path_status():
                    global _agent
                    if _agent and _agent_ready:
                        mods = str(_agent.mods_dir) if _agent.mods_dir else "未检测到"
                        logf = str(_agent.log_file) if _agent.log_file else "未检测到"
                        _refs["path_status"].set_content(
                            f'<div style="font-size:0.8em;color:#888;margin-top:4px;">'
                            f'Mods 文件夹: <code style="color:#4ade80;">{mods}</code><br>'
                            f'日志文件: <code style="color:#4ade80;">{logf}</code>'
                            f'</div>'
                        )

                async def on_generate():
                    global _agent
                    user_input = prompt_textarea.value.strip()
                    if not user_input:
                        ui.notify("请输入 Mod 描述。", type="warning")
                        return
                    if not _agent_ready:
                        ui.notify("智能体仍在加载中，请稍候...", type="warning")
                        return

                    generate_btn.disable()
                    spinner.set_visibility(True)
                    gen_status.set_visibility(True)
                    gen_status.set_text("正在生成...")
                    stages_view.set_content(_all_stages_html(WorkflowStage.PARSE))

                    api_key = api_key_input.value.strip() or None
                    provider = provider_select.value
                    model = model_input.value.strip() or None
                    dlc_version = dlc_select.value
                    selected_libraries = []
                    if curlib_check.value:
                        selected_libraries.append("Curlib")
                    if rgon_check.value:
                        selected_libraries.append("RGON")

                    try:
                        result = await _agent.run(
                            user_input,
                            api_key=api_key,
                            provider=provider if api_key else None,
                            model=model,
                            dlc_version=dlc_version,
                            libraries=selected_libraries,
                        )
                    except Exception as e:
                        ui.notify(f"生成失败: {e}", type="error")
                        generate_btn.enable()
                        spinner.set_visibility(False)
                        gen_status.set_visibility(False)
                        stages_view.set_content(_all_stages_html(WorkflowStage.ERROR))
                        return

                    stages_view.set_content(_all_stages_html(result.stage))

                    msgs = getattr(result, "messages", []) or []
                    msg_html = "<br>".join(
                        f"{'🤖' if m.get('role') == 'agent' else '⚙️'} "
                        f"{m.get('content', '')}"
                        for m in msgs[-8:]
                    )
                    messages_view.set_content(msg_html or "无消息")

                    if result.generated_code:
                        codes = []
                        for a in result.generated_code:
                            codes.append(
                                f"-- {'=' * 50}\n"
                                f"-- 模板: {a.scaffold_type}\n"
                                f"-- {'=' * 50}\n\n{a.lua_code}"
                            )
                        code_viewer.set_content("\n\n".join(codes))

                        # Auto-build and output to mods folder
                        try:
                            from isaac_agent.build import ModBuilder
                            builder = ModBuilder(agent=_agent)
                            safe_name = "".join(
                                c if c.isalnum() or c in "_-" else "_"
                                for c in (result.task.title if result.task else "isaac_mod")
                            ).strip("_").lower() or "isaac_mod"
                            mod_path = builder.build_from_agent_result(result, mod_name=safe_name)
                            build_msg = f"已输出到 Mods 文件夹: {mod_path}"
                            gen_status.set_text(
                                f"完成 — {len(result.generated_code)} 个产出，"
                                f"{build_msg}"
                            )
                        except Exception as build_err:
                            gen_status.set_text(
                                f"完成 — {len(result.generated_code)} 个产出，"
                                f"阶段: {result.stage.value}"
                            )
                            logger.warning(f"Build to mods failed: {build_err}")
                    else:
                        code_viewer.set_content("-- 未生成代码")
                        gen_status.set_text("完成 — 未生成代码")

                    generate_btn.enable()
                    spinner.set_visibility(False)

                    if result.errors:
                        ui.notify("\n".join(result.errors), type="warning")

                with ui.row().classes("items-center gap-3"):
                    generate_btn = ui.button(
                        "⚡ 生成 Mod 代码",
                        on_click=on_generate,
                    ).classes("bg-primary text-white")
                    if not _agent_ready:
                        generate_btn.disable()
                    _refs["generate_btn"] = generate_btn
                    spinner = ui.spinner(size="sm")
                    spinner.set_visibility(False)
                    gen_status = ui.label("")
                    gen_status.set_visibility(False)

                # Log analysis button
                async def on_analyze_log():
                    global _agent
                    if not _agent_ready:
                        ui.notify("智能体仍在加载中...", type="warning")
                        return

                    current_code = code_viewer.content if hasattr(code_viewer, 'content') else ""
                    try:
                        analysis = _agent.analyze_log_errors(
                            source_code=current_code,
                            mod_name="isaac_mod",
                        )
                    except Exception as e:
                        ui.notify(f"日志分析失败: {e}", type="error")
                        return

                    if analysis.get("fixable"):
                        ui.notify(f"发现可修复错误: {analysis['summary']}", type="info")
                        if analysis.get("fixed_code"):
                            code_viewer.set_content(analysis["fixed_code"])
                    elif analysis.get("errors"):
                        ui.notify(f"无法自动修复: {analysis['summary']}", type="warning")
                        if analysis.get("debug_code"):
                            code_viewer.set_content(analysis["debug_code"])
                    else:
                        ui.notify(analysis.get("summary", "未发现 Lua 错误"), type="info")

                with ui.row().classes("items-center gap-3"):
                    ui.button(
                        "🔍 分析日志错误",
                        on_click=on_analyze_log,
                    ).props("outline")
                    ui.button("📍 刷新路径", on_click=_update_path_status).props("outline")

            # -- API Search + Templates tabs --
            with ui.tabs() as tabs:
                api_tab = ui.tab("API 搜索")
                tmpl_tab = ui.tab("模板")

            with ui.tab_panels(tabs, value=api_tab).classes("w-full"):
                # ---- API Search tab ----
                with ui.tab_panel(api_tab):
                    results_table = ui.table(
                        columns=[
                            {"name": "function", "label": "函数", "field": "function"},
                            {"name": "category", "label": "分类", "field": "category"},
                            {"name": "score", "label": "评分", "field": "score"},
                        ],
                        rows=[],
                    ).classes("w-full")
                    results_table.set_visibility(False)

                    api_detail = ui.html("")

                    async def do_search():
                        global _agent
                        query = search_input.value.strip()
                        if not query or _agent is None:
                            return
                        try:
                            results = _agent.api_search_tool.search(query)
                        except Exception:
                            ui.notify("搜索失败", type="error")
                            return
                        rows = []
                        for r in results:
                            name = r.get("function_name") or r.get("function", "?")
                            cat = r.get("category") or r.get("class", "?")
                            score = r.get("score", 0)
                            rows.append({
                                "function": name,
                                "category": cat,
                                "score": f"{score:.1f}" if isinstance(score, float) else str(score),
                            })
                        results_table.rows = rows
                        results_table.set_visibility(len(rows) > 0)
                        if results:
                            _show_detail(results[0], api_detail)

                    with ui.row().classes("gap-2 items-end w-full"):
                        search_input = ui.input(
                            placeholder="搜索 API（例如 AddHearts）...",
                        ).classes("flex-grow")
                        search_input.on("keydown.enter", do_search)
                        ui.button("搜索", on_click=do_search)

                # ---- Templates tab ----
                with ui.tab_panel(tmpl_tab):
                    _refs["template_container"] = ui.element("div")
                    with _refs["template_container"]:
                        _build_template_tab()

        # ============================================== RIGHT COLUMN
        with ui.column().classes("w-3/5 gap-4"):
            with ui.card().classes("w-full"):
                ui.label("工作流管道").classes("text-lg font-bold")
                stages_view = ui.html(_all_stages_html(None))
                ui.separator()
                ui.label("消息:").classes("text-sm text-grey")
                messages_view = ui.html("")

            with ui.card().classes("w-full flex-grow"):
                ui.label("生成的代码").classes("text-lg font-bold")
                code_viewer = ui.code(
                    "-- 生成的 Lua 代码将显示在这里...",
                    language="lua",
                ).classes("w-full min-h-[300px]")

    # ---- Agent readiness polling (auto-enables UI when agent finishes init) ----
    def _on_agent_ready():
        if not _agent_ready:
            return
        _refs["loading_badge"].set_visibility(False)
        _refs["ready_badge"].set_visibility(True)
        _refs["generate_btn"].enable()
        tc = _refs.get("template_container")
        if tc is not None:
            tc.clear()
            with tc:
                _build_template_tab()
        _update_path_status()
        _refs["_ready_timer"].deactivate()

    if not _agent_ready:
        _refs["_ready_timer"] = ui.timer(2.0, _on_agent_ready)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _show_detail(info: dict, view: ui.html):
    name = info.get("function_name") or info.get("function", "?")
    desc = info.get("description", "无描述")
    returns = info.get("return_type", "void")
    params = info.get("parameters", [])
    example = info.get("example_code", "")

    html = f"<b>{name}</b><br><i>{desc}</i><br><br>"
    html += f"<b>返回值:</b> <code>{returns}</code><br>"
    if params:
        html += "<b>参数:</b><ul>"
        for p in params:
            if isinstance(p, dict):
                html += f"<li><code>{p.get('name', '?')}</code>: {p.get('type', '?')}</li>"
            else:
                html += f"<li>{p}</li>"
        html += "</ul>"
    if example:
        html += f"<b>示例:</b><pre><code>{example}</code></pre>"
    view.set_content(html)


def _build_template_tab():
    global _agent, _agent_ready
    if not _agent_ready or not _agent:
        ui.label("智能体加载中，模板即将显示...").classes("text-grey")
        return
    manager = _agent.template_manager
    names = manager.list_templates()

    template_select = (
        ui.select(options=names, value=names[0] if names else None, label="选择模板")
        .classes("w-full")
    )
    preview = ui.code("", language="lua").classes("w-full min-h-[200px]")

    def update_preview():
        if not manager:
            return
        name = template_select.value
        if name:
            desc = manager.get_template_description(name)
            code = manager.get_template(name)
            preview.set_content(f"-- {name}: {desc}\n{code}")

    template_select.on("update:model-value", update_preview)
    update_preview()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    # reload is disabled in Docker (USE_RELOAD=false) — the watchdog process
    # breaks port binding inside containers
    ui.run(
        title="Isaac AI Agent",
        host="0.0.0.0",
        port=8080,
        reload=os.environ.get("USE_RELOAD", "").lower() in ("1", "true", "yes"),
        show=False,
        language="zh-CN",
    )


if __name__ in ("__main__", "__mp_main__"):
    main()
