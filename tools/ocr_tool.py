from tools.base_tool import BaseTool


class OcrTool(BaseTool):
    def execute(self, payload):
        return {"status": "ok"}