from tools.mcp.base_mcp import BaseMCP


class N8nMCP(BaseMCP):
    def __init__(self):
        super().__init__(name="n8n_mcp", status="active")

    def execute(self, payload):
        return {
            "mcp": self.name,
            "status": self.status,
            "action": "n8n workflow trigger simulated",
            "payload": payload,
        }