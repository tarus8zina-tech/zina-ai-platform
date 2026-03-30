from datetime import datetime
from pathlib import Path
import subprocess
import streamlit as st

from core.orchestrator import Orchestrator
from core.agent_loader import load_agents
from core.tool_loader import load_tools
from core.workflow_loader import load_workflows

from tools.tool_registry import ToolRegistry
from workflows.workflow_registry import WorkflowRegistry
from tools.mcp.mcp_registry import McpRegistry
from tools.mcp.n8n_mcp import N8nMCP

from dashboard.components.styles import inject_css
from dashboard.components.overview import render_overview
from dashboard.components.agent_panel import render_agents_page
from dashboard.components.tool_panel import render_tools_page
from dashboard.components.workflow_panel import render_workflows_page
from dashboard.components.mcp_panel import render_mcp_page
from dashboard.components.system_status import render_system_page
from dashboard.components.next_steps import render_next_steps_page


@st.cache_resource
def setup_platform():
    orchestrator = Orchestrator()
    load_agents(orchestrator.registry)

    tool_registry = ToolRegistry()
    load_tools(tool_registry)

    workflow_registry = WorkflowRegistry()
    load_workflows(workflow_registry)

    mcp_registry = McpRegistry()
    mcp_registry.register_mcp("n8n_mcp", N8nMCP())

    hotel_agent = orchestrator.registry.get_agent("hotel_agent")
    if hotel_agent is not None:
        mock_tool = tool_registry.get_tool("mock_data_tool")
        if mock_tool is not None and hasattr(hotel_agent, "set_tool"):
            hotel_agent.set_tool(mock_tool)

    return orchestrator, tool_registry, workflow_registry, mcp_registry


def _render_sidebar(agent_count: int, tool_count: int, workflow_count: int) -> str:
    with st.sidebar:
        st.markdown(
            """
            <div style="font-size:1.3rem;font-weight:700;color:#2f2a26;margin-bottom:0.1rem;">◈ Zina AI</div>
            <div style="font-size:0.78rem;color:#8a7e76;margin-bottom:1rem;">AI Operating System</div>
            """,
            unsafe_allow_html=True,
        )

        page = st.radio(
            "nav",
            [
                "Overview",
                "Agents",
                "Tools",
                "Workflows",
                "MCP & Integrations",
                "System Status",
                "Next Steps",
            ],
            label_visibility="collapsed",
        )

        st.markdown(
            f"""
            <div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid #cdbfb0;">
                <div style="font-size:0.72rem;color:#8a7e76;margin-bottom:0.4rem;text-transform:uppercase;letter-spacing:0.06em;">Quick stats</div>
                <div style="font-size:0.82rem;color:#4d443d;">
                    {agent_count} agents &nbsp;·&nbsp; {tool_count} tools<br>
                    {workflow_count} workflows
                </div>
            </div>
            <div style="margin-top:1.2rem;font-size:0.72rem;color:#a0958a;">
                v0.1.0 &nbsp;·&nbsp; {datetime.now().strftime("%H:%M")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    return page


def main():
    st.set_page_config(
        page_title="Zina AI Platform",
        page_icon="◈",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

    orchestrator, tool_registry, workflow_registry, mcp_registry = setup_platform()

    overview = orchestrator.registry.overview()
    agent_names = overview["agents"]
    tool_names = tool_registry.overview()
    workflow_names = workflow_registry.overview()
    mcp_names = mcp_registry.overview()

    page = _render_sidebar(
        agent_count=len(agent_names),
        tool_count=len(tool_names),
        workflow_count=len(workflow_names),
    )

    if page == "Overview":
        render_overview(orchestrator, tool_registry, workflow_registry, mcp_registry)

    elif page == "Agents":
        render_agents_page(orchestrator, agent_names)

    elif page == "Tools":
        render_tools_page(tool_names)

    elif page == "Workflows":
        render_workflows_page(workflow_registry, workflow_names, orchestrator)

    elif page == "MCP & Integrations":
        render_mcp_page(mcp_registry, mcp_names)

    elif page == "System Status":
        render_system_page(orchestrator, tool_names, workflow_names, mcp_names)

    elif page == "Next Steps":
        render_next_steps_page()

    _render_task_generator()


def _render_task_generator():
    st.markdown("---")
    st.header("🤖 GPT → Claude Task Generator")

    user_input = st.text_area(
        "Describe what Claude should build",
        placeholder="e.g. A summary report of all hotel bookings from last month",
        height=120,
        key="task_gen_input",
    )

    if st.button("Generate Claude Task", key="task_gen_button"):
        if user_input.strip():
            st.session_state["task_gen_prompt"] = f"""You are a system execution agent.

Decide where to save the file:

- If the request is about an AGENT → save in: agents/
- If it's documentation → save in: docs/
- Otherwise → default to: docs/

An agent is:
- something that performs tasks
- has logic or responsibilities
- interacts with tools or workflows

Now execute this request:

{user_input.strip()}

IMPORTANT:
- Actually create the file
- Save it in the correct folder
- Return the final result and file path
"""
        else:
            st.warning("Please enter a description first.")

    if "task_gen_prompt" in st.session_state:
        prompt = st.session_state["task_gen_prompt"]
        st.code(prompt, language="markdown")

        if st.button("Run in Claude", key="task_gen_run"):
            task_file = Path("claude_task.txt")
            task_file.write_text(prompt, encoding="utf-8")

            with st.spinner("Running Claude..."):
                try:
                    result = subprocess.run(
                        ["claude"],
                        stdin=task_file.open("r", encoding="utf-8"),
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )
                    if result.returncode == 0:
                        st.success("Claude responded:")
                        st.code(result.stdout or "(no output)", language="markdown")
                    else:
                        st.error("Claude exited with an error:")
                        st.code(result.stderr or "(no error details)", language="bash")
                except FileNotFoundError:
                    st.error("`claude` CLI not found. Make sure Claude Code is installed and on your PATH.")
                except subprocess.TimeoutExpired:
                    st.error("Claude did not respond within 120 seconds.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
