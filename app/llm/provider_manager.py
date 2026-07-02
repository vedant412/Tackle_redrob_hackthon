from app.llm.gemini_provider import GeminiProvider
from app.llm.groq_provider import GroqProvider


class ProviderManager:

    def __init__(self):

        self.providers = [
            GeminiProvider(),
            GroqProvider(),
        ]

    def generate(
        self,
        prompt: str,
        response_schema=None,
        temperature: float = 0.2,
    ):

        last_error = None

        for provider in self.providers:

            try:

                print(f"Using {provider.name}")

                return provider.generate(
                    prompt=prompt,
                    response_schema=response_schema,
                    temperature=temperature,
                )

            except Exception as e:

                print(f"{provider.name} failed: {e}")

                last_error = e

        raise RuntimeError(
            f"All providers failed.\nLast error: {last_error}"
        )