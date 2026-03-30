from core.orchestrator import Orchestrator
from core.agent_loader import load_agents
from core.tool_loader import load_tools
from core.workflow_loader import load_workflows

from tools.tool_registry import ToolRegistry
from workflows.workflow_registry import WorkflowRegistry


def test_workflows_load():
    workflow_registry = WorkflowRegistry()
    load_workflows(workflow_registry)

    overview = workflow_registry.overview()

    print("Loaded workflows:", overview)

    assert "hotel_workflow" in overview


def test_hotel_workflow_run():
    orchestrator = Orchestrator()
    load_agents(orchestrator.registry)

    tool_registry = ToolRegistry()
    load_tools(tool_registry)

    hotel_agent = orchestrator.registry.get_agent("hotel_agent")
    if hotel_agent is not None:
        hotel_agent.set_tool(tool_registry.get_tool("mock_data_tool"))

    workflow_registry = WorkflowRegistry()
    load_workflows(workflow_registry)

    workflow = workflow_registry.get_workflow("hotel_workflow")
    result = workflow.run("Analyze hotel booking performance", orchestrator)

    print("Workflow result:", result)

    assert result["workflow"] == "hotel_workflow"
    assert result["status"] == "completed"
    assert result["agent_result"]["status"] == "success"