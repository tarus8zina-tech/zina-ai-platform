import streamlit as st

# MCP metadata — both registered and planned
MCP_REGISTERED = {
    "n8n_mcp": {
        "description": "Connects to n8n for workflow automation and webhook triggering.",
        "status": "registered",
        "docs_url": "https://n8n.io/docs",
    },
}

MCP_PLANNED = [
    {
        "name": "github_mcp",
        "description": "Read and write GitHub issues, PRs, and repository data.",
        "status": "planned",
    },
    {
        "name": "ocr_mcp",
        "description": "OCR processing pipeline for documents and images via MCP.",
        "status": "planned",
    },
    {
        "name": "notion_mcp",
        "description": "Sync data and notes with Notion workspaces.",
        "status": "planned",
    },
    {
        "name": "slack_mcp",
        "description": "Send notifications and receive commands via Slack.",
        "status": "planned",
    },
    {
        "name": "google_workspace_mcp",
        "description": "Access Gmail, Calendar, and Drive through MCP.",
        "status": "planned",
    },
]

INTEGRATION_STATUS = [
    {"name": "n8n", "type": "Automation", "status": "active", "note": "Registered via MCP"},
    {"name": "GitHub", "type": "Dev Tools", "status": "placeholder", "note": "Tool available, MCP planned"},
    {"name": "Google Ads", "type": "Marketing", "status": "placeholder", "note": "Tool available, MCP planned"},
    {"name": "CRM", "type": "Sales", "status": "placeholder", "note": "Tool available, connection pending"},
]


def _status_badge(status: str) -> str:
    if status == "active":
        return '<span class="badge badge-green">active</span>'
    if status == "registered":
        return '<span class="badge badge-green">registered</span>'
    if status == "planned":
        return '<span class="placeholder-badge">planned</span>'
    return '<span class="badge badge-gray">placeholder</span>'


def render_mcp_page(mcp_registry, mcp_names: list):
    st.markdown('<div class="page-title">MCP & Integrations</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Model Context Protocol connections and external integrations</div>',
        unsafe_allow_html=True,
    )

    # Info banner
    st.info(
        "MCP (Model Context Protocol) allows agents to access external tools and data sources "
        "in a structured, permission-controlled way. Active connections are listed below."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">ACTIVE MCPs</div>
                <div class="metric-value">{len(mcp_names)}</div>
                <div class="metric-sub">Registered & online</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">PLANNED MCPs</div>
                <div class="metric-value">{len(MCP_PLANNED)}</div>
                <div class="metric-sub">On roadmap</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">INTEGRATIONS</div>
                <div class="metric-value">{len(INTEGRATION_STATUS)}</div>
                <div class="metric-sub">Connected & planned</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Active MCP Connections</div>', unsafe_allow_html=True)

        if mcp_names:
            for name in mcp_names:
                meta = MCP_REGISTERED.get(name, {"description": "MCP connection.", "status": "registered"})
                st.markdown(
                    f"""
                    <div class="mcp-card">
                        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.25rem;">
                            <span class="mcp-name">{name}</span>
                            {_status_badge(meta["status"])}
                        </div>
                        <div class="mcp-desc">{meta["description"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No MCP connections registered.")

        st.markdown('<div class="section-title" style="margin-top:1rem;">Planned MCPs</div>', unsafe_allow_html=True)
        for mcp in MCP_PLANNED:
            st.markdown(
                f"""
                <div class="mcp-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.25rem;">
                        <span class="mcp-name">{mcp["name"]}</span>
                        {_status_badge(mcp["status"])}
                    </div>
                    <div class="mcp-desc">{mcp["description"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Integration Status</div>', unsafe_allow_html=True)

        for integration in INTEGRATION_STATUS:
            st.markdown(
                f"""
                <div class="list-row">
                    <div>
                        <div class="row-name">{integration["name"]}</div>
                        <div class="row-desc">{integration["note"]}</div>
                    </div>
                    <div style="text-align:right;">
                        <div>{_status_badge(integration["status"])}</div>
                        <div style="font-size:0.72rem;color:#8a7e76;margin-top:0.2rem;">{integration["type"]}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-box" style="margin-top:1rem;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">What is MCP?</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size:0.85rem;color:#6e655d;line-height:1.6;">
            Model Context Protocol (MCP) is an open standard that lets AI agents connect
            to external data sources and tools in a secure, structured way.<br><br>
            Each MCP server exposes tools and resources that agents can call with
            full permission control — no raw API keys in prompts.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
