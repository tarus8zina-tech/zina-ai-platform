from tools.base_tool import BaseTool


class WebSearchTool(BaseTool):
    def execute(self, payload):
        return {"status": "ok"}