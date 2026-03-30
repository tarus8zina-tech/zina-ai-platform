class McpRegistry:
    def __init__(self):
        self.mcps = {}

    def register_mcp(self, name, mcp):
        self.mcps[name] = mcp

    def get_mcp(self, name):
        return self.mcps.get(name)

    def overview(self):
        return list(self.mcps.keys())

    def status_overview(self):
        return {
            name: mcp.info()
            for name, mcp in self.mcps.items()
        }