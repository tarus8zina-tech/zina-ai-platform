import os
import anthropic


class GeneralAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-opus-4-6"

    def run(self, task: str) -> dict:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=(
                "You are Zina, a helpful AI assistant embedded in a local AI platform. "
                "Respond concisely and directly to the task."
            ),
            messages=[
                {"role": "user", "content": task}
            ],
        )

        text = next(
            (block.text for block in response.content if block.type == "text"),
            "",
        )

        return {
            "agent": "general_agent",
            "model": self.model,
            "task": task,
            "response": text,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
