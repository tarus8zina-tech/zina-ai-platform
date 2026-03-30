from tools.base_tool import BaseTool


class MockDataTool(BaseTool):
    def execute(self, payload):
        return {
            "source": "mock_data_tool",
            "payload": payload,
            "data": [
                {"name": "Hotel Oberhausen", "occupancy": 78, "revenue": 4200},
                {"name": "Hotel Moers", "occupancy": 64, "revenue": 3150},
                {"name": "Hotel Krefeld", "occupancy": 81, "revenue": 4630},
            ],
        }