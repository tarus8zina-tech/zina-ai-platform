import streamlit as st

# Static metadata for registered tools — extend as new tools are added
TOOL_META = {
    # Core tools
    "file_tool": {
        "description": "Read and write files on the local filesystem",
        "category": "Core",
    },
    "report_tool": {
        "description": "Generate structured reports from agent output",
        "category": "Core",
    },
    "mock_data_tool": {
        "description": "Generate mock data for testing and development",
        "category": "Core",
    },
    "web_search_tool": {
        "description": "Search the web for real-time information",
        "category": "Research",
    },
    "ocr_tool": {
        "description": "Extract text from images and PDF files via OCR",
        "category": "Processing",
    },
    "email_tool": {
        "description": "Compose and send emails via configured provider",
        "category": "Communication",
    },
    # Integrations
    "crm_tool": {
        "description": "Read and write data to CRM systems",
        "category": "Integration",
    },
    "github_tool": {
        "description": "Interact with GitHub repositories and issues",
        "category": "Integration",
    },
    "google_ads_tool": {
        "description": "Query and manage Google Ads campaigns",
        "category": "Integration",
    },
    "n8n_tool": {
        "description": "Trigger n8n automation workflows via webhook",
        "category": "Integration",
    },
}

_DEFAULT_TOOL_META = {"description": "Registered tool.", "category": "Other"}

_CATEGORY_ORDER = ["Core", "Research", "Processing", "Communication", "Integration", "Other"]


def render_tools_page(tool_names: list):
    st.markdown('<div class="page-title">Tools</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">All tools loaded into the platform, grouped by category</div>',
        unsafe_allow_html=True,
    )

    # Build count summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">TOTAL TOOLS</div>
                <div class="metric-value">{len(tool_names)}</div>
                <div class="metric-sub">Currently loaded</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        integration_count = sum(
            1 for n in tool_names if TOOL_META.get(n, _DEFAULT_TOOL_META)["category"] == "Integration"
        )
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">INTEGRATIONS</div>
                <div class="metric-value">{integration_count}</div>
                <div class="metric-sub">External services</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        core_count = sum(
            1 for n in tool_names if TOOL_META.get(n, _DEFAULT_TOOL_META)["category"] == "Core"
        )
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">CORE TOOLS</div>
                <div class="metric-value">{core_count}</div>
                <div class="metric-sub">Platform essentials</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-sep"></div>', unsafe_allow_html=True)

    # Group tools by category
    by_category: dict[str, list[str]] = {}
    for name in tool_names:
        cat = TOOL_META.get(name, _DEFAULT_TOOL_META)["category"]
        by_category.setdefault(cat, []).append(name)

    left_col, right_col = st.columns(2)
    cols = [left_col, right_col]
    col_idx = 0

    for cat in _CATEGORY_ORDER:
        names = by_category.get(cat)
        if not names:
            continue
        with cols[col_idx % 2]:
            st.markdown(f'<div class="tool-category-header">{cat}</div>', unsafe_allow_html=True)
            for name in names:
                meta = TOOL_META.get(name, _DEFAULT_TOOL_META)
                st.markdown(
                    f"""
                    <div class="tool-row">
                        <div>
                            <div class="tool-name">{name}</div>
                            <div class="tool-desc">{meta["description"]}</div>
                        </div>
                        <span class="cat-tag">{meta["category"]}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        col_idx += 1

    # Any uncategorized tools not in metadata
    unknown = [n for n in tool_names if n not in TOOL_META]
    if unknown:
        st.markdown('<div class="tool-category-header">Other</div>', unsafe_allow_html=True)
        for name in unknown:
            st.markdown(
                f"""
                <div class="tool-row">
                    <div>
                        <div class="tool-name">{name}</div>
                        <div class="tool-desc">Registered tool.</div>
                    </div>
                    <span class="cat-tag">Other</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
