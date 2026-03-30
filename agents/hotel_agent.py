from agents.base_agent import BaseAgent


class HotelAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.tool = None

    def set_tool(self, tool):
        self.tool = tool

    def run(self, task):
        if self.tool is None:
            return f"Hotel Agent processed task without tool: {task}"

        tool_result = self.tool.execute(task)

        hotels = tool_result.get("data", [])
        total_revenue = sum(item["revenue"] for item in hotels)
        avg_occupancy = sum(item["occupancy"] for item in hotels) / len(hotels)

        return {
            "message": f"Hotel Agent analyzed task: {task}",
            "source": tool_result.get("source"),
            "hotels_analyzed": len(hotels),
            "total_revenue": total_revenue,
            "average_occupancy": round(avg_occupancy, 2),
        }