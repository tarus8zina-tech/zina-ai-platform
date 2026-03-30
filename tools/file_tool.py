from tools.base_tool import BaseTool


class FileTool(BaseTool):
    def execute(self, payload):
        return {"status": "ok"}