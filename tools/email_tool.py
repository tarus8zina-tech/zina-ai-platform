from tools.base_tool import BaseTool


class EmailTool(BaseTool):
    def execute(self, payload):
        return {"status": "ok"}