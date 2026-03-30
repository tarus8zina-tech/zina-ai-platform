from core.orchestrator import Orchestrator
from core.agent_loader import load_agents


def test_agents_load():
    orchestrator = Orchestrator()
    load_agents(orchestrator.registry)

    overview = orchestrator.registry.overview()

    print("Loaded agents:", overview["agents"])

    assert "general_agent" in overview["agents"]
    assert "hotel_agent" in overview["agents"]
    assert "document_agent" in overview["agents"]
    assert "business_dev_agent" in overview["agents"]
    assert "finance_agent" in overview["agents"]


def test_agent_routing():
    orchestrator = Orchestrator()
    load_agents(orchestrator.registry)

    response = orchestrator.handle_task("Analyze hotel booking performance")

    print("Routing response:", response)

    assert response["status"] == "success"
    assert response["selected_agent"] == "hotel_agent"