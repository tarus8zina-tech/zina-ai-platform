class Router:
    def __init__(self, default_agent: str = "general_agent") -> None:
        self.default_agent = default_agent

    def route(self, task: str) -> str:
        task_lower = task.lower()

        # Social media keywords are checked first — they are specific enough
        # to override other domain matches (e.g. "hotel instagram post")
        if any(word in task_lower for word in ["instagram", "social media", "caption", "hashtag", "carousel", "reel"]):
            return "zina_content_creator_agent"

        if any(word in task_lower for word in ["hotel", "booking", "guest", "reservation"]):
            return "hotel_agent"

        if any(word in task_lower for word in ["document", "pdf", "invoice", "contract"]):
            return "document_agent"

        if any(word in task_lower for word in ["lead", "outreach", "sales", "business"]):
            return "business_dev_agent"

        if any(word in task_lower for word in ["finance", "cost", "profit", "revenue"]):
            return "finance_agent"

        # "content" and "post" are generic — only route to content creator
        # when no other domain matched first
        if any(word in task_lower for word in ["content", "post"]):
            return "zina_content_creator_agent"

        return self.default_agent