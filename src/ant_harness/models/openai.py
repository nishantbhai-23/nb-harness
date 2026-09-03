import os
from typing import Any, List

from openai import OpenAI
from ant_harness.models.model_base import ModelBase, ModelConfig, PromptConfig


class OpenAIModel(ModelBase):
    def __init__(self, model_config: ModelConfig):
        api_key = os.environ.get("OPENAI_API_KEY", "")
        super().__init__(api_key)
        self.model_config = model_config
        self.client = OpenAI(api_key=api_key)

    def call(self, messages: List[Any]) -> Any:
        try:
            response = self.client.chat.completions.create(
                model=self.model_config.model,
                messages=messages,
                max_tokens=self.model_config.max_tokens,
                timeout=self.model_config.response_timeout_ms / 1000
            )
            self.calculate_and_accumulate_cost(response)
            return response
        except Exception as e:
            raise e

    def chat(self, messages: List[Any]) -> str:
        """Send the full messages array and return just the assistant content string."""
        response = self.call(messages)
        return response.choices[0].message.content

    def generate(self, prompt_template, data_points: List[Any]) -> Any:
        messages = []
        for data_point in data_points:
            message = prompt_template.format(**data_point)
            messages.append(message)
        return self.call(messages)

    def calculate_and_accumulate_cost(self, response) -> float:
        if response.usage:
            self.total_cost_incurred += response.usage.total_tokens * 0.002