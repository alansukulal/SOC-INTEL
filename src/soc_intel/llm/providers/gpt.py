from typing import TypeVar

from openai import OpenAI
from pydantic import BaseModel

from soc_intel.llm.base import LLMClient


T = TypeVar("T", bound=BaseModel)


class GPTClient(LLMClient):
    def __init__(
        self,
        api_key: str,
        model: str,
    ) -> None:
        self.api_key = api_key
        self.model = model

        self.client = OpenAI(
            api_key=self.api_key,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        if not response.output_text:
            raise ValueError(
                "OpenAI returned an empty response."
            )

        return response.output_text

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:
        response = self.client.responses.parse(
            model=self.model,
            input=prompt,
            text_format=response_model,
        )

        if response.output_parsed is None:
            raise ValueError(
                "OpenAI returned an empty structured response."
            )

        return response.output_parsed