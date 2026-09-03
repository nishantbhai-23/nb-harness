from abc import abstractmethod
from ..models.model_base import ModelConfig, get_model
from ..logging.logger import Logger
from ..checkpoints.checkpoint import CheckPoint

class Agent:
    def __init__(self, model_config: ModelConfig, max_attempts = 3, data_points: list[any] = []):
        self.model = get_model(model_config)
        self.max_attempts = max_attempts
        self.current_attempts = 0
        self.logger = Logger()
        self.checkpoint = CheckPoint("./checkpoints")
        self.messages = []
        self.data_points = data_points

    @abstractmethod
    def attempt(self):
        """
        This method should be called to make a single attempt at the task.
        """
        pass

    @abstractmethod
    def start(self):
        """
        This method should be called to start the agent loop.
        It should keep calling attempt() until the agent decides to stop.
        It should also handle the case where the agent needs to be retried.
        """
        pass
