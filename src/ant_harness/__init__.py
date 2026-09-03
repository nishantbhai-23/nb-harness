import os
from dotenv import load_dotenv
from .models.model_base import ModelConfig
from .agents.football import FootballAgent


def main():
    # Load environment variables
    load_dotenv()

    # Configure model
    model_config = ModelConfig(model="gpt-4.1-nano")

    # Resolve prompt path
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        "prompts", "football_agent", "basic_prompt.yaml"
    )

    # Create and start the agent
    agent = FootballAgent(
        model_config=model_config,
        prompt_path=prompt_path,
        max_attempts=50
    )
    agent.start()
