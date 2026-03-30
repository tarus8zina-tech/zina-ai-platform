class Router:
    def __init__(self, default_agent: str = "general_agent") -> None:
        self.default_agent = default_agent

    def route(self, task: str) -> str:
        task_lower = task.lower()

        if any(word in task_lower for word in ["hotel", "booking", "guest", "reservation"]):
            return "hotel_agent"

        if any(word in task_lower for word in ["document", "pdf", "invoice", "contract"]):
            return "document_agent"

        if any(word in task_lower for word in ["lead", "outreach", "sales", "business"]):
            return "business_dev_agent"

        if any(word in task_lower for word in ["finance", "cost", "profit", "revenue"]):
            return "finance_agent"

        return self.default_agent