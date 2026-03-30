import streamlit as st

NEXT_STEPS = [
    {
        "priority": "high",
        "title": "Connect Claude API to all agents",
        "description": "Replace stub run() methods with real Anthropic API calls using tool_use.",
        "area": "Agents",
    },
    {
        "priority": "high",
        "title": "Implement Human-in-the-Loop approval flow",
        "description": "Before any agent sends email or modifies data, require explicit user confirmation.",
        "area": "Core",
    },
    {
        "priority": "high",
        "title": "Add MCP server connections",
        "description": "Spin up and connect GitHub MCP, OCR MCP and test with real requests.",
        "area": "MCP",
    },
    {
        "priority": "medium",
        "title": "Agent memory & state persistence",
        "description": "Store conversation history and task results so agents have context across runs.",
        "area": "Core",
    },
    {
        "priority": "medium",
        "title": "Build multi-step workflow editor",
        "description": "UI to define, chain, and visualize workflow steps without editing code.",
        "area": "Workflows",
    },
    {
        "priority": "medium",
        "title": "Connect CRM integration",
        "description": "Wire up crm_tool to a real CRM (HubSpot / Salesforce) with read/write.",
        "area": "Integrations",
    },
    {
        "priority": "medium",
        "title": "Add audit logging",
        "description": "Log every agent invocation, tool call, and result with timestamps to file/DB.",
        "area": "Core",
    },
    {
        "priority": "low",
        "title": "Extend router with ML-based routing",
        "description": "Replace keyword matching with embedding-based semantic routing.",
        "area": "Router",
    },
    {
        "priority": "low",
        "title": "Add agent scheduling",
        "description": "Allow workflows and tasks to be scheduled via cron or time triggers.",
        "area": "Workflows",
    },
    {
        "priority": "low",
        "title": "Build lead_research_agent full pipeline",
        "description": "Combine web_search_tool + report_tool + email_tool into a full lead workflow.",
        "area": "Agents",
    },
]

_AREA_COLORS = {
    "Agents": "#dbe7d7",
    "Core": "#d7e3f0",
    "MCP": "#e0d8f0",
    "Workflows": "#e8ddf0",
    "Integrations": "#f0e6d6",
    "Router": "#e8e4df",
}
_AREA_BORDER = {
    "Agents": "#9eb495",
    "Core": "#8aaacf",
    "MCP": "#b8a8d8",
    "Workflows": "#b89ecf",
    "Integrations": "#c9a87a",
    "Router": "#c4bdb6",
}
_AREA_TEXT = {
    "Agents": "#345139",
    "Core": "#2a4a6b",
    "MCP": "#4a3a6b",
    "Workflows": "#4a2a6b",
    "Integrations": "#7a5230",
    "Router": "#6e665f",
}


def _area_tag(area: str) -> str:
    bg = _AREA_COLORS.get(area, "#e8e4df")
    border = _AREA_BORDER.get(area, "#c4bdb6")
    color = _AREA_TEXT.get(area, "#6e665f")
    return (
        f'<span style="font-size:0.7rem;padding:0.15rem 0.5rem;border-radius:999px;'
        f'background:{bg};border:1px solid {border};color:{color};white-space:nowrap;">'
        f"{area}</span>"
    )


def _priority_badge(priority: str) -> str:
    cls = f"task-priority priority-{priority}"
    return f'<span class="{cls}">{priority.upper()}</span>'


def render_next_steps_page():
    st.markdown('<div class="page-title">Next Steps</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Planned improvements and open tasks for the Zina AI Platform</div>',
        unsafe_allow_html=True,
    )

    high = [t for t in NEXT_STEPS if t["priority"] == "high"]
    medium = [t for t in NEXT_STEPS if t["priority"] == "medium"]
    low = [t for t in NEXT_STEPS if t["priority"] == "low"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">HIGH PRIORITY</div>
                <div class="metric-value">{len(high)}</div>
                <div class="metric-sub">Do next</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">MEDIUM PRIORITY</div>
                <div class="metric-value">{len(medium)}</div>
                <div class="metric-sub">Coming soon</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">LOW PRIORITY</div>
                <div class="metric-value">{len(low)}</div>
                <div class="metric-sub">Backlog</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)

    # Filter by area
    all_areas = sorted(set(t["area"] for t in NEXT_STEPS))
    selected_area = st.selectbox(
        "Filter by area",
        ["All"] + all_areas,
        label_visibility="visible",
    )

    filtered = NEXT_STEPS if selected_area == "All" else [t for t in NEXT_STEPS if t["area"] == selected_area]

    for group_label, group_priority in [("High Priority", "high"), ("Medium Priority", "medium"), ("Low Priority", "low")]:
        group_tasks = [t for t in filtered if t["priority"] == group_priority]
        if not group_tasks:
            continue
        st.markdown(f'<div class="section-title" style="margin-top:0.8rem;">{group_label}</div>', unsafe_allow_html=True)
        for task in group_tasks:
            st.markdown(
                f"""
                <div class="task-item">
                    <div style="display:flex;flex-direction:column;gap:0.3rem;min-width:70px;">
                        {_priority_badge(task["priority"])}
                        {_area_tag(task["area"])}
                    </div>
                    <div>
                        <div class="task-title">{task["title"]}</div>
                        <div class="task-desc">{task["description"]}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
