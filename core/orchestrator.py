from core.config import config
from core.registry import Registry
from core.router import Router


class Orchestrator:
    def __init__(self) -> None:
        self.registry = Registry()
        self.router = Router(default_agent=config.default_agent)

    def handle_task(self, task: str) -> dict:
        selected_agent_name = self.router.route(task)
        selected_agent = self.registry.get_agent(selected_agent_name)

        if selected_agent is None:
            return {
                "status": "error",
                "task": task,
                "selected_agent": selected_agent_name,
                "message": f"No agent registered with name '{selected_agent_name}'.",
            }

        result = selected_agent.run(task)

        return {
            "status": "success",
            "task": task,
            "selected_agent": selected_agent_name,
            "result": result,
        }