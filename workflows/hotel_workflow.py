from workflows.base_workflow import BaseWorkflow


class HotelWorkflow(BaseWorkflow):
    def run(self, task, orchestrator):
        response = orchestrator.handle_task(task)

        return {
            "workflow": "hotel_workflow",
            "task": task,
            "status": "completed",
            "agent_result": response,
        }