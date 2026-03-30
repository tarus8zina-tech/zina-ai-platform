from tools.mcp.mcp_registry import McpRegistry
from tools.mcp.n8n_mcp import N8nMcp


def test_mcp_registry():
    registry = McpRegistry()
    registry.register_mcp("n8n_mcp", N8nMcp())

    overview = registry.overview()
    status = registry.status_overview()

    print("Loaded MCPs:", overview)
    print("MCP Status:", status)

    assert "n8n_mcp" in overview
    assert status["n8n_mcp"]["status"] == "active"


if __name__ == "__main__":
    test_mcp_registry()