import streamlit as st
from datetime import datetime


CORE_MODULES = [
    {"name": "orchestrator", "file": "core/orchestrator.py", "status": "online", "role": "Central task coordinator"},
    {"name": "router", "file": "core/router.py", "status": "online", "role": "Keyword-based task routing"},
    {"name": "registry", "file": "core/registry.py", "status": "online", "role": "Agent/tool/workflow store"},
    {"name": "agent_loader", "file": "core/agent_loader.py", "status": "online", "role": "Loads agents into registry"},
    {"name": "tool_loader", "file": "core/tool_loader.py", "status": "online", "role": "Loads tools into registry"},
    {"name": "workflow_loader", "file": "core/workflow_loader.py", "status": "online", "role": "Loads workflows"},
    {"name": "state_manager", "file": "core/state_manager.py", "status": "online", "role": "Session state management"},
    {"name": "mcp_registry", "file": "tools/mcp/mcp_registry.py", "status": "online", "role": "MCP connection registry"},
    {"name": "dashboard", "file": "dashboard/streamlit_app.py", "status": "online", "role": "Web UI (Streamlit)"},
]


def _status_dot(status: str) -> str:
    if status == "online":
        return '<span style="color:#4a7c5a;">●</span>'
    if status == "degraded":
        return '<span style="color:#c8a870;">●</span>'
    return '<span style="color:#c87070;">●</span>'


def render_system_page(orchestrator, tool_names: list, workflow_names: list, mcp_names: list):
    st.markdown('<div class="page-title">System Status</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Core module health, registry overview, and routing diagnostics</div>',
        unsafe_allow_html=True,
    )

    online_count = sum(1 for m in CORE_MODULES if m["status"] == "online")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">CORE MODULES</div>
                <div class="metric-value">{online_count}/{len(CORE_MODULES)}</div>
                <div class="metric-sub">Online</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">REGISTRY</div>
                <div class="metric-value">{len(tool_names) + len(workflow_names)}</div>
                <div class="metric-sub">Tools + Workflows</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">MCP CONNECTIONS</div>
                <div class="metric-value">{len(mcp_names)}</div>
                <div class="metric-sub">Active</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        now = datetime.now().strftime("%H:%M")
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">UPTIME</div>
                <div class="metric-value" style="font-size:1.4rem;">{now}</div>
                <div class="metric-sub">Session active</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Core Modules</div>', unsafe_allow_html=True)
        for module in CORE_MODULES:
            st.markdown(
                f"""
                <div class="list-row">
                    <div>
                        <div class="row-name">{_status_dot(module["status"])} &nbsp;{module["name"]}</div>
                        <div class="row-desc">{module["role"]} · <code style="font-size:0.72rem;color:#8a7e76;">{module["file"]}</code></div>
                    </div>
                    <div class="row-status status-active">{module["status"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        # Registry overview
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Registry</div>', unsafe_allow_html=True)

        overview = orchestrator.registry.overview()
        sections = [
            ("Agents", overview["agents"], "active"),
            ("Tools", tool_names, "loaded"),
            ("Workflows", workflow_names, "ready"),
            ("MCPs", mcp_names, "active"),
        ]
        for label, items, status in sections:
            st.markdown(
                f'<div style="font-size:0.75rem;font-weight:700;color:#8a7e76;text-transform:uppercase;letter-spacing:0.07em;margin:0.6rem 0 0.3rem 0;">{label} ({len(items)})</div>',
                unsafe_allow_html=True,
            )
            for item in items:
                st.markdown(
                    f"""
                    <div class="list-row" style="padding:0.4rem 0.7rem;">
                        <div class="row-name" style="font-size:0.82rem;">{item}</div>
                        <div class="row-status status-{status}" style="font-size:0.7rem;">{status}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

        # Routing preview
        st.markdown('<div class="section-box" style="margin-top:1rem;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Routing Preview</div>', unsafe_allow_html=True)
        preview_tasks = [
            "Analyze hotel bookings",
            "Parse invoice PDF",
            "Research new leads",
            "Review finance report",
            "General system check",
        ]
        for task in preview_tasks:
            agent = orchestrator.router.route(task)
            st.markdown(
                f"""
                <div class="routing-item">
                    <span style="font-size:0.8rem;">{task}</span><br>
                    → <span class="routing-agent">{agent}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
