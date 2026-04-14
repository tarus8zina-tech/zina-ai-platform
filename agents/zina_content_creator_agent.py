import os
import json
import anthropic

SYSTEM_PROMPT = """You are Zina Content Creator, an expert Instagram content strategist and copywriter.
You create scroll-stopping content for brands across all industries.

For every request, return a single valid JSON object — no markdown, no code blocks, just raw JSON.

Schema:
{
  "brand": "brand name, or 'General' if not specified",
  "content_type": "post" | "carousel" | "reel" | "story",
  "tone": "casual" | "professional" | "inspirational" | "educational" | "humorous",
  "hook": "first line that stops the scroll — under 10 words, punchy",
  "caption": "full Instagram caption with line breaks and emojis, 150-300 chars",
  "call_to_action": "one specific CTA that drives engagement or conversion",
  "hashtags": ["#tag1", "#tag2"],  // 12-15 relevant hashtags, mix of sizes
  "post_ideas": [                  // 3 alternative content angles for this brief
    "idea 1",
    "idea 2",
    "idea 3"
  ],
  "carousel": null,                // null unless content_type is "carousel"
  "notes": "1-2 sentences on strategy or best posting time"
}

For content_type "carousel", set carousel to:
{
  "slide_count": 5,
  "slides": [
    {"slide": 1, "title": "Cover — hook title", "text": "teaser line"},
    {"slide": 2, "title": "slide title", "text": "body copy"},
    ...
    {"slide": 5, "title": "CTA slide", "text": "closing + action"}
  ]
}

For content_type "reel", add a "reel" key:
{
  "reel": {
    "opening_scene": "first 3 seconds visual description",
    "script_beats": ["beat 1", "beat 2", "beat 3"],
    "text_overlays": ["overlay 1", "overlay 2"],
    "audio_suggestion": "trending audio style or specific vibe"
  }
}

Rules:
- Always write in the brand voice if a brand is mentioned
- Hashtags must be relevant, not generic spam
- Hooks must create curiosity or emotion
- CTAs must be specific: "comment your city below", not just "leave a comment"
"""


class ZinaContentCreatorAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-opus-4-6"

    def run(self, task: str) -> dict:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": task}
            ],
        )

        raw = next(
            (block.text for block in response.content if block.type == "text"),
            "{}",
        )

        try:
            content = json.loads(raw)
        except json.JSONDecodeError:
            # Claude occasionally wraps JSON in a code block — strip it
            cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            try:
                content = json.loads(cleaned)
            except json.JSONDecodeError:
                content = {"raw_response": raw, "parse_error": "Could not parse JSON"}

        return {
            "agent": "zina_content_creator_agent",
            "model": self.model,
            "task": task,
            "content": content,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
