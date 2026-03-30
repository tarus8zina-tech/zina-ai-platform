from tools.tool_registry import ToolRegistry
from core.tool_loader import load_tools


def test_tools_load():
    tool_registry = ToolRegistry()
    load_tools(tool_registry)

    overview = tool_registry.overview()

    print("Loaded tools:", overview)

    assert "mock_data_tool" in overview


def test_mock_data_tool_execute():
    tool_registry = ToolRegistry()
    load_tools(tool_registry)

    tool = tool_registry.get_tool("mock_data_tool")
    result = tool.execute("Analyze hotel booking performance")

    print("Tool result:", result)

    assert result["source"] == "mock_data_tool"
    assert len(result["data"]) == 3