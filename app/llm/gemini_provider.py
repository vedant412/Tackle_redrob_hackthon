import time

from google import genai
from google.genai.errors import ServerError

from app.config import GEMINI_API_KEY
from app.config import GEMINI_MODEL
from app.llm.base_provider import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):

    @property
    def name(self):

        return "Gemini"

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(
        self,
        prompt: str,
        response_schema=None,
        temperature: float = 0.2,
    ):

        config = {
            "temperature": temperature
        }

        if response_schema is not None:

            config["response_mime_type"] = "application/json"
            config["response_schema"] = response_schema

        retries = 4

        for attempt in range(retries):

            try:

                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config=config,
                )

                return response.text

            except ServerError:

                if attempt == retries - 1:
                    raise

                wait = 2 ** attempt

                print(f"[Gemini] Busy. Retrying in {wait}s...")

                time.sleep(wait)