from app.llm.gemini_provider import GeminiProvider
from app.llm.groq_provider import GroqProvider


class LLMRouter:

    def __init__(self):

        self.providers = [

            GeminiProvider(),

            GroqProvider(),

        ]

    def generate(
        self,
        prompt,
        response_schema=None,
        temperature=0.2,
    ):

        last_exception = None

        for provider in self.providers:

            try:

                print(f"\nUsing {provider.name}")

                return provider.generate(
                    prompt=prompt,
                    response_schema=response_schema,
                    temperature=temperature,
                )

            except Exception as e:

                print(f"{provider.name} failed")

                print(e)

                last_exception = e

        raise last_exception