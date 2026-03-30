from agents.base_agent import BaseAgent


class LeadResearchAgent(BaseAgent):
    def run(self, task):
        return f"Lead Research Agent processed task: {task}"