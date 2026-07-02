from groq import Groq

from app.config import GROQ_API_KEY
from app.config import GROQ_MODEL
from app.llm.base_provider import BaseLLMProvider


class GroqProvider(BaseLLMProvider):

    @property
    def name(self):
        return "Groq"

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def generate(
        self,
        prompt: str,
        response_schema=None,
        temperature: float = 0.2,
    ):

        # Groq requires the prompt/messages to explicitly mention JSON
        system_prompt = """
You are a structured information extraction assistant.

IMPORTANT RULES:
- Always return ONLY valid JSON.
- Never return Markdown.
- Never wrap JSON inside ``` blocks.
- Never explain your answer.
- The response must be parseable by json.loads().
"""

        user_prompt = f"""
Return ONLY valid JSON.

{prompt}
"""

        completion = self.client.chat.completions.create(

            model=GROQ_MODEL,

            temperature=temperature,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],

            response_format={
                "type": "json_object"
            },

        )

        return completion.choices[0].message.content