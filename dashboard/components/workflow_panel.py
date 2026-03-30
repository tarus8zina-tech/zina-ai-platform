import streamlit as st

WORKFLOW_META = {
    "hotel_workflow": {
        "description": "End-to-end hotel analytics — booking data, occupancy, and revenue summary.",
        "steps": ["Fetch booking data", "Analyze occupancy", "Calculate revenue", "Generate report"],
    },
}

_DEFAULT_WORKFLOW_META = {
    "description": "Registered workflow.",
    "steps": [],
}


def render_workflows_page(workflow_registry, workflow_names: list, orchestrator):
    st.markdown('<div class="page-title">Workflows</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Multi-step automated workflows ready for execution</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">WORKFLOWS REGISTERED</div>
                <div class="metric-value">{len(workflow_names)}</div>
                <div class="metric-sub">Ready to execute</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)

    if not workflow_names:
        st.info("No workflows registered.")
        return

    list_col, run_col = st.columns([1, 1])

    with list_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Registered Workflows</div>', unsafe_allow_html=True)
        for name in workflow_names:
            meta = WORKFLOW_META.get(name, _DEFAULT_WORKFLOW_META)
            steps_html = ""
            for i, step in enumerate(meta.get("steps", []), 1):
                steps_html += f'<div style="font-size:0.76rem;color:#8a7e76;margin-top:0.15rem;">{i}. {step}</div>'

            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-name">{name}</div>
                    <div class="agent-desc" style="margin-top:0.3rem;">{meta["description"]}</div>
                    {steps_html}
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with run_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Execute Workflow</div>', unsafe_allow_html=True)

        selected_wf = st.selectbox(
            "Select workflow",
            workflow_names,
            label_visibility="collapsed",
            key="wf_page_select",
        )
        wf_task = st.text_area(
            "Task input",
            value="Analyze hotel booking performance",
            height=100,
            label_visibility="collapsed",
            key="wf_page_task",
        )

        if st.button("Run Workflow", key="wf_page_run"):
            wf = workflow_registry.get_workflow(selected_wf)
            if wf is not None:
                with st.spinner(f"Running {selected_wf}..."):
                    result = wf.run(wf_task, orchestrator)
                st.success("Workflow complete")
                st.json(result)
            else:
                st.error("Workflow not found in registry.")

        st.markdown("</div>", unsafe_allow_html=True)
