from core.orchestrator import Orchestrator
from core.agent_loader import load_agents
from core.tool_loader import load_tools
from core.workflow_loader import load_workflows

from tools.tool_registry import ToolRegistry
from workflows.workflow_registry import WorkflowRegistry


def main():
    orchestrator = Orchestrator()
    load_agents(orchestrator.registry)

    tool_registry = ToolRegistry()
    load_tools(tool_registry)

    workflow_registry = WorkflowRegistry()
    load_workflows(workflow_registry)

    hotel_agent = orchestrator.registry.get_agent("hotel_agent")
    if hotel_agent is not None:
        hotel_agent.set_tool(tool_registry.get_tool("mock_data_tool"))

    demo_tasks = [
        "Analyze hotel booking performance",
        "Read this PDF invoice",
        "Find new business leads",
        "Review monthly finance costs",
        "Do a general system check",
    ]

    for task in demo_tasks:
        response = orchestrator.handle_task(task)
        print(response)

    print("\n--- WORKFLOW TEST ---")

    hotel_workflow = workflow_registry.get_workflow("hotel_workflow")
    if hotel_workflow is not None:
        workflow_result = hotel_workflow.run("Analyze hotel booking performance", orchestrator)
        print(workflow_result)


if __name__ == "__main__":
    main()