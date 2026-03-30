from tools.base_tool import BaseTool


class ReportTool(BaseTool):
    def execute(self, payload):
        return {"status": "ok"}