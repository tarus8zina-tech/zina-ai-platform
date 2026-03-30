import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        /* ===== BASE ===== */
        .stApp { background-color: #f5f1eb; color: #2f2a26; }
        .block-container { padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1450px; }
        h1, h2, h3, h4, h5, h6, p, label, div, span { color: #2f2a26; }

        /* ===== TYPOGRAPHY ===== */
        .page-title { font-size: 1.7rem; font-weight: 700; color: #2f2a26; margin-bottom: 0.25rem; }
        .page-subtitle { font-size: 0.9rem; color: #6e655d; margin-bottom: 1.4rem; }
        .zina-title { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.15rem; color: #2f2a26; }
        .zina-subtitle { font-size: 0.95rem; color: #6e655d; margin-bottom: 1.2rem; }

        /* ===== TOPBAR ===== */
        .topbar {
            display: flex; justify-content: space-between; align-items: center;
            gap: 1rem; padding: 0.8rem 1.2rem;
            background: #e7dfd6; border: 2px solid #cdbfb0;
            border-radius: 14px; margin-bottom: 1.2rem;
        }
        .topbar-left { font-size: 1.0rem; font-weight: 700; color: #2f2a26; }
        .topbar-right { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }

        /* ===== BADGES ===== */
        .badge { padding: 0.3rem 0.65rem; border-radius: 999px; font-size: 0.8rem; border: 1px solid #bba999; background: #f7f3ee; color: #4d443d; }
        .badge-green { background: #dbe7d7; border: 1px solid #9eb495; color: #345139; }
        .badge-orange { background: #f0e6d6; border: 1px solid #c9a87a; color: #7a5230; }
        .badge-gray { background: #e8e4df; border: 1px solid #c4bdb6; color: #6e665f; }

        /* ===== METRIC CARDS ===== */
        .metric-card {
            background: #e7dfd6; border: 2px solid #cdbfb0;
            border-radius: 16px; padding: 1.1rem 1.2rem; min-height: 120px;
        }
        .metric-title { font-size: 0.78rem; color: #6e655d; letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 0.55rem; }
        .metric-value { font-size: 2.1rem; font-weight: 700; color: #2f2a26; }
        .metric-sub { font-size: 0.76rem; color: #8a7e76; margin-top: 0.25rem; }

        /* ===== SYSTEM STRIP ===== */
        .system-strip { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.8rem 0 1.2rem 0; }
        .system-pill { padding: 0.38rem 0.72rem; border-radius: 999px; border: 1px solid #cdbfb0; background: #efe7de; color: #4d443d; font-size: 0.78rem; }
        .system-pill-ok { background: #dbe7d7; border: 1px solid #9eb495; color: #345139; }

        /* ===== SECTION BOX ===== */
        .section-box { background: #ece4db; border: 2px solid #cdbfb0; border-radius: 16px; padding: 1.1rem; height: 100%; margin-bottom: 1rem; }
        .section-title { font-size: 0.85rem; font-weight: 700; color: #2f2a26; margin-bottom: 0.75rem; padding-bottom: 0.45rem; border-bottom: 1px solid #cdbfb0; text-transform: uppercase; letter-spacing: 0.06em; }

        /* ===== LIST ROWS ===== */
        .list-row { display: flex; justify-content: space-between; align-items: center; gap: 0.8rem; padding: 0.65rem 0.85rem; margin-bottom: 0.5rem; border-radius: 10px; background: #f8f4ef; border: 1px solid #cdbfb0; }
        .row-name { font-weight: 500; color: #2f2a26; font-size: 0.88rem; }
        .row-desc { font-size: 0.76rem; color: #7a7068; margin-top: 0.15rem; }
        .row-status { font-size: 0.75rem; padding: 0.18rem 0.5rem; border-radius: 999px; white-space: nowrap; }
        .status-active { background: #dbe7d7; border: 1px solid #9eb495; color: #345139; }
        .status-loaded { background: #d7e3f0; border: 1px solid #8aaacf; color: #2a4a6b; }
        .status-ready { background: #e8ddf0; border: 1px solid #b89ecf; color: #4a2a6b; }
        .status-placeholder { background: #e8e4df; border: 1px solid #c4bdb6; color: #6e665f; }

        /* ===== MASTER AGENT CARD ===== */
        .master-agent-card {
            background: #2f2a26; color: #f5f1eb;
            border-radius: 18px; padding: 1.5rem 1.6rem; margin-bottom: 1.2rem;
        }
        .master-agent-label { font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase; color: #a0958a; margin-bottom: 0.35rem; }
        .master-agent-title { font-size: 1.55rem; font-weight: 700; color: #f5f1eb; margin-bottom: 0.45rem; }
        .master-agent-desc { font-size: 0.88rem; color: #c8bfb5; margin-bottom: 1rem; line-height: 1.55; }
        .master-agent-stats { display: flex; gap: 1.5rem; flex-wrap: wrap; }
        .master-stat-value { font-size: 1.35rem; font-weight: 700; color: #f5f1eb; }
        .master-stat-label { font-size: 0.7rem; color: #a0958a; text-transform: uppercase; letter-spacing: 0.06em; }

        /* ===== AGENT CARDS ===== */
        .agent-card { background: #f8f4ef; border: 1.5px solid #cdbfb0; border-radius: 14px; padding: 1rem 1.1rem; margin-bottom: 0.75rem; }
        .agent-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; }
        .agent-name { font-weight: 700; font-size: 0.9rem; color: #2f2a26; font-family: monospace; }
        .agent-type { font-size: 0.72rem; padding: 0.15rem 0.5rem; border-radius: 999px; background: #e7dfd6; border: 1px solid #cdbfb0; color: #6e655d; }
        .agent-desc { font-size: 0.82rem; color: #6e655d; margin-bottom: 0.5rem; line-height: 1.45; }
        .agent-caps { display: flex; gap: 0.35rem; flex-wrap: wrap; }
        .cap-tag { font-size: 0.7rem; padding: 0.18rem 0.48rem; border-radius: 999px; background: #dbe7d7; border: 1px solid #9eb495; color: #345139; }

        /* ===== TOOL ROWS ===== */
        .tool-category-header { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #8a7e76; margin: 1rem 0 0.45rem 0; padding-bottom: 0.25rem; border-bottom: 1px dashed #cdbfb0; }
        .tool-row { display: flex; justify-content: space-between; align-items: center; padding: 0.62rem 0.85rem; margin-bottom: 0.45rem; border-radius: 10px; background: #f8f4ef; border: 1px solid #cdbfb0; }
        .tool-name { font-weight: 600; font-size: 0.85rem; color: #2f2a26; font-family: monospace; }
        .tool-desc { font-size: 0.76rem; color: #7a7068; }
        .cat-tag { font-size: 0.7rem; padding: 0.15rem 0.48rem; border-radius: 999px; background: #e0d8f0; border: 1px solid #b8a8d8; color: #4a3a6b; white-space: nowrap; }

        /* ===== MCP CARDS ===== */
        .mcp-card { background: #f8f4ef; border: 1.5px solid #cdbfb0; border-radius: 14px; padding: 1rem 1.1rem; margin-bottom: 0.7rem; }
        .mcp-name { font-weight: 700; font-family: monospace; font-size: 0.9rem; color: #2f2a26; margin-bottom: 0.25rem; }
        .mcp-desc { font-size: 0.82rem; color: #6e655d; }
        .placeholder-badge { font-size: 0.72rem; padding: 0.18rem 0.55rem; border-radius: 999px; background: #f0e8d8; border: 1px solid #c8a870; color: #7a5a2a; }

        /* ===== ROUTING ===== */
        .routing-item { padding: 0.7rem 0.9rem; margin-bottom: 0.5rem; border-radius: 10px; background: #f8f4ef; border: 1px solid #cdbfb0; font-size: 0.85rem; }
        .routing-agent { color: #6d5b4d; font-weight: 700; font-family: monospace; }

        /* ===== TASK ITEMS ===== */
        .task-item { display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.8rem 0.9rem; margin-bottom: 0.55rem; border-radius: 10px; background: #f8f4ef; border: 1px solid #cdbfb0; }
        .task-priority { font-size: 0.7rem; padding: 0.18rem 0.48rem; border-radius: 999px; white-space: nowrap; font-weight: 600; }
        .priority-high { background: #f0d8d8; border: 1px solid #c89898; color: #6b2a2a; }
        .priority-medium { background: #f0e8d8; border: 1px solid #c8a870; color: #7a5a2a; }
        .priority-low { background: #e8e4df; border: 1px solid #c4bdb6; color: #6e665f; }
        .task-title { font-weight: 600; font-size: 0.88rem; color: #2f2a26; }
        .task-desc { font-size: 0.78rem; color: #7a7068; margin-top: 0.18rem; }

        /* ===== INPUTS ===== */
        .stTextArea textarea, .stTextInput input {
            background-color: #f8f4ef !important; color: #2f2a26 !important;
            border: 1px solid #cdbfb0 !important; border-radius: 10px !important;
        }
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #f8f4ef !important; color: #2f2a26 !important;
            border: 1px solid #cdbfb0 !important; border-radius: 10px !important;
        }
        .stButton > button {
            width: 100%; background: #b8a999; color: #2f2a26;
            border-radius: 10px; border: 1px solid #a79383;
            padding: 0.62rem 1rem; font-weight: 700; font-size: 0.88rem;
        }
        .stButton > button:hover { background: #a79383; color: white; }

        /* ===== MISC ===== */
        .section-sep { margin: 1.4rem 0; border-top: 1px solid #d7cbbf; }
        hr { border-color: #d7cbbf; }
        section[data-testid="stSidebar"] { background: #e7dfd6; border-right: 2px solid #cdbfb0; }
        div[data-testid="stAlert"] { border-radius: 12px; }
        </style>
        """,
        unsafe_allow_html=True,
    )
