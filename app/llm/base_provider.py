from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def generate(
        self,
        prompt: str,
        response_schema=None,
        temperature: float = 0.2,
    ):
        pass