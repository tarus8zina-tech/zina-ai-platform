from datetime import datetime
import streamlit as st


def render_header():
    st.markdown('<div class="zina-title">Zina AI Platform</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="zina-subtitle">AI Operating System — Agents · Tools · Workflows · Human-in-the-Loop</div>',
        unsafe_allow_html=True,
    )


def render_topbar():
    current_time = datetime.now().strftime("%H:%M:%S")
    st.markdown(
        f"""
        <div class="topbar">
            <div class="topbar-left">◈ Zina AI Platform</div>
            <div class="topbar-right">
                <span class="badge badge-green">● System healthy</span>
                <span class="badge">Core online</span>
                <span class="badge">Human-in-the-loop</span>
                <span class="badge">{current_time}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards(agent_count, tool_count, workflow_count, mcp_count):
    c1, c2, c3, c4, c5 = st.columns(5)

    cards = [
        (c1, "AGENTS", agent_count, "Registered sub-agents"),
        (c2, "TOOLS", tool_count, "Loaded & available"),
        (c3, "WORKFLOWS", workflow_count, "Ready to execute"),
        (c4, "MCPs", mcp_count, "Integrations active"),
        (c5, "SYSTEM", "ON", "All core modules up"),
    ]

    for col, title, value, sub in cards:
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_system_strip():
    modules = [
        ("orchestrator", True),
        ("agent_loader", True),
        ("tool_loader", True),
        ("workflow_loader", True),
        ("mcp_registry", True),
        ("router", True),
        ("dashboard", True),
    ]
    html = '<div class="system-strip">'
    for name, ok in modules:
        cls = "system-pill system-pill-ok" if ok else "system-pill"
        html += f'<span class="{cls}">● {name}</span>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_quick_command(orchestrator, workflow_registry, workflow_names):
    st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)
    cmd_col, wf_col = st.columns(2)

    with cmd_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Command Center</div>', unsafe_allow_html=True)
        task = st.text_area(
            "Task input",
            value="Analyze hotel booking performance",
            height=110,
            key="overview_task",
            label_visibility="collapsed",
        )
        if st.button("Run Task", key="overview_run_task"):
            with st.spinner("Running..."):
                response = orchestrator.handle_task(task)
            st.success(f"Handled by: **{response.get('selected_agent', '—')}**")
            st.json(response)
        st.markdown("</div>", unsafe_allow_html=True)

    with wf_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Workflow Center</div>', unsafe_allow_html=True)
        if workflow_names:
            selected_wf = st.selectbox(
                "Workflow",
                workflow_names,
                key="overview_wf_select",
                label_visibility="collapsed",
            )
            wf_task = st.text_input(
                "Workflow input",
                value="Analyze hotel booking performance",
                key="overview_wf_task",
                label_visibility="collapsed",
            )
            if st.button("Run Workflow", key="overview_run_wf"):
                wf = workflow_registry.get_workflow(selected_wf)
                if wf is not None:
                    with st.spinner("Running workflow..."):
                        result = wf.run(wf_task, orchestrator)
                    st.success("Workflow complete")
                    st.json(result)
                else:
                    st.error("Workflow not found.")
        else:
            st.info("No workflows registered.")
        st.markdown("</div>", unsafe_allow_html=True)


def render_overview(orchestrator, tool_registry, workflow_registry, mcp_registry):
    render_header()
    render_topbar()

    overview = orchestrator.registry.overview()
    agent_names = overview["agents"]
    tool_names = tool_registry.overview()
    workflow_names = workflow_registry.overview()
    mcp_names = mcp_registry.overview()

    render_metric_cards(
        agent_count=len(agent_names),
        tool_count=len(tool_names),
        workflow_count=len(workflow_names),
        mcp_count=len(mcp_names),
    )
    render_system_strip()

    # Quick summary panels
    st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    panels = [
        (c1, "Agents", agent_names, "active"),
        (c2, "Tools", tool_names, "loaded"),
        (c3, "Workflows", workflow_names, "ready"),
        (c4, "MCPs", mcp_names, "active"),
    ]

    for col, title, items, status in panels:
        with col:
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
            if items:
                for item in items:
                    st.markdown(
                        f"""
                        <div class="list-row">
                            <div class="row-name">{item}</div>
                            <div class="row-status status-{status}">{status}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("None registered.")
            st.markdown("</div>", unsafe_allow_html=True)

    render_quick_command(orchestrator, workflow_registry, workflow_names)
