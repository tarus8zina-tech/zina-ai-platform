import streamlit as st

# Static metadata for registered agents — extend as new agents are added
AGENT_META = {
    "hotel_agent": {
        "description": "Analyzes hotel booking data, occupancy rates, and guest performance metrics.",
        "capabilities": ["Booking analysis", "Occupancy metrics", "Revenue tracking"],
        "keywords": ["hotel", "booking", "guest", "reservation"],
        "type": "Specialized",
    },
    "document_agent": {
        "description": "Processes and extracts information from documents, PDFs, invoices, and contracts.",
        "capabilities": ["PDF reading", "Invoice parsing", "Contract review"],
        "keywords": ["document", "pdf", "invoice", "contract"],
        "type": "Specialized",
    },
    "business_dev_agent": {
        "description": "Handles business development tasks including lead research and sales strategy.",
        "capabilities": ["Lead generation", "Sales analysis", "Outreach planning"],
        "keywords": ["lead", "outreach", "sales", "business"],
        "type": "Specialized",
    },
    "finance_agent": {
        "description": "Analyzes financial data — costs, profits, revenue, and budget performance.",
        "capabilities": ["Cost analysis", "Revenue tracking", "Financial reports"],
        "keywords": ["finance", "cost", "profit", "revenue"],
        "type": "Specialized",
    },
    "general_agent": {
        "description": "Fallback agent for general queries and tasks not matched by specialized agents.",
        "capabilities": ["General queries", "System checks", "Fallback routing"],
        "keywords": ["general", "default", "misc"],
        "type": "General",
    },
    "lead_research_agent": {
        "description": "Deep-dives into lead research, contact qualification, and data enrichment.",
        "capabilities": ["Lead research", "Contact qualification", "Data enrichment"],
        "keywords": ["lead", "research", "contact"],
        "type": "Specialized",
    },
}

_DEFAULT_META = {
    "description": "Agent registered in the system.",
    "capabilities": [],
    "keywords": [],
    "type": "Unknown",
}


def _render_master_agent_card(agent_count: int, tool_count: int, workflow_count: int):
    st.markdown(
        f"""
        <div class="master-agent-card">
            <div class="master-agent-label">Master Agent</div>
            <div class="master-agent-title">Orchestrator</div>
            <div class="master-agent-desc">
                The Orchestrator is the central coordinator of the Zina AI Platform.
                It receives tasks, routes them to the most suitable sub-agent via the Router,
                and returns structured results. Human-in-the-loop is preserved at every step.
            </div>
            <div class="master-agent-stats">
                <div>
                    <div class="master-stat-value">{agent_count}</div>
                    <div class="master-stat-label">Sub-Agents</div>
                </div>
                <div>
                    <div class="master-stat-value">{tool_count}</div>
                    <div class="master-stat-label">Tools Available</div>
                </div>
                <div>
                    <div class="master-stat-value">{workflow_count}</div>
                    <div class="master-stat-label">Workflows</div>
                </div>
                <div>
                    <div class="master-stat-value">ON</div>
                    <div class="master-stat-label">Status</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_router_info():
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Router Logic</div>', unsafe_allow_html=True)
    routing_rules = [
        ("hotel, booking, guest, reservation", "hotel_agent"),
        ("document, pdf, invoice, contract", "document_agent"),
        ("lead, outreach, sales, business", "business_dev_agent"),
        ("finance, cost, profit, revenue", "finance_agent"),
        ("(anything else)", "general_agent"),
    ]
    for keywords, agent in routing_rules:
        st.markdown(
            f"""
            <div class="routing-item">
                <span style="color:#8a7e76;font-size:0.78rem;">{keywords}</span>
                <br>→ <span class="routing-agent">{agent}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def _render_sub_agent_card(name: str, meta: dict):
    caps_html = "".join(
        f'<span class="cap-tag">{c}</span>' for c in meta.get("capabilities", [])
    )
    st.markdown(
        f"""
        <div class="agent-card">
            <div class="agent-card-header">
                <span class="agent-name">{name}</span>
                <span class="agent-type">{meta.get("type", "Unknown")}</span>
            </div>
            <div class="agent-desc">{meta.get("description", "")}</div>
            <div class="agent-caps">{caps_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_agents_page(orchestrator, agent_names: list):
    st.markdown('<div class="page-title">Agents</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Master Orchestrator + registered Sub-Agents</div>',
        unsafe_allow_html=True,
    )

    tool_count = len(orchestrator.registry.tools)
    workflow_count = len(orchestrator.registry.workflows)

    _render_master_agent_card(
        agent_count=len(agent_names),
        tool_count=tool_count,
        workflow_count=workflow_count,
    )

    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Sub-Agents</div>', unsafe_allow_html=True)
        if agent_names:
            for name in agent_names:
                meta = AGENT_META.get(name, _DEFAULT_META)
                _render_sub_agent_card(name, meta)
        else:
            st.info("No sub-agents registered.")
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        _render_router_info()

        st.markdown('<div class="section-box" style="margin-top:1rem;">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Route Preview</div>', unsafe_allow_html=True)
        preview_tasks = [
            "Analyze hotel booking",
            "Read invoice PDF",
            "Find sales leads",
            "Review finance costs",
            "General system check",
        ]
        for t in preview_tasks:
            routed = orchestrator.router.route(t)
            st.markdown(
                f"""
                <div class="routing-item">
                    <span style="font-size:0.82rem;">{t}</span><br>
                    → <span class="routing-agent">{routed}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
