from typing import List, Any
from abc import ABC, abstractmethod
from enum import StrEnum


class SupportedModel(StrEnum):
    GPT_4_1_NANO = "gpt-4.1-nano"
    GPT_4_1_MINI = "gpt-4.1-mini"

class ModelConfig:
    def __init__(self, model: SupportedModel, max_tokens =25000, response_timeout_ms=30000):
        self.model = SupportedModel(model)
        self.max_tokens = max_tokens
        self.response_timeout_ms = response_timeout_ms

class PromptConfig:
    def __init__(self, system_prompt, instruction_prompt):
        self.system_prompt = system_prompt
        self.instruction_prompt = instruction_prompt

class ModelBase(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.total_cost_incurred = 0.0
        

    @abstractmethod
    def call(self, messages: List[Any]) -> Any:
        """
        This method takes the raw messages as input, and returns the raw response from the provider.
        The messages should be in the format of the provider.
        """
        pass

    @abstractmethod
    def chat(self, messages: List[Any]) -> str:
        """
        Takes the full messages array (with role/content dicts) and returns
        just the assistant's response content string.
        """
        pass

    @abstractmethod
    def generate(self, prompt_template, data_points: List[Any]) -> Any:
        """
        This method should take in the prompt template and data points, format them into messages 
        which could be sent to the provider endpoint
        """
        pass

    @abstractmethod
    def calculate_and_accumulate_cost(self, response):
        """
        Calculate cost for each inference. Should always automatically be called within 'call'
        on each succesfull call
        """
        pass


def get_model(model_config: ModelConfig):
    from ant_harness.models.openai import OpenAIModel

    _MODEL_REGISTRY = {
        SupportedModel.GPT_4_1_NANO: OpenAIModel,
        SupportedModel.GPT_4_1_MINI: OpenAIModel,
    }

    model_cls = _MODEL_REGISTRY.get(model_config.model)
    if model_cls is None:
        raise ValueError(f"Unsupported model: {model_config.model}")
    return model_cls(model_config)