from typing import TypeVar

from google import genai
from pydantic import BaseModel

from soc_intel.llm.base import LLMClient


T = TypeVar("T", bound=BaseModel)


class GeminiClient(LLMClient):
    def __init__(
        self,
        api_key: str,
        model: str,
    ) -> None:
        self.api_key = api_key
        self.model = model

        self.client = genai.Client(
            api_key=self.api_key,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        return response.text

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": response_model,
            },
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty structured response."
            )

        return response_model.model_validate_json(
            response.text
        )