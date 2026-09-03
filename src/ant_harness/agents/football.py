import yaml
import os

from .agent_base import Agent
from ..models.model_base import ModelConfig, PromptConfig


class FootballAgent(Agent):
    def __init__(self, model_config: ModelConfig, prompt_path: str, max_attempts: int = 50):
        super().__init__(model_config, max_attempts)

        # Load prompt YAML
        self.logger.log(f"Loading prompt from: {prompt_path}")
        with open(prompt_path, "r") as f:
            prompt_data = yaml.safe_load(f)

        system_prompt = prompt_data["agent"]["system_template"].strip()
        instruction_prompt = prompt_data["agent"]["instance_template"].strip()

        # Seed messages with system + instruction prompts
        self.messages.append({"role": "system", "content": system_prompt})
        self.messages.append({"role": "system", "content": instruction_prompt})
        self.logger.log("System and instruction prompts loaded into messages.")

    def attempt(self) -> str:
        """Send the full messages array to the model and append the response."""
        self.logger.log(f"Sending {len(self.messages)} messages to model (attempt {self.current_attempts + 1})...")
        response_content = self.model.chat(self.messages)
        self.messages.append({"role": "assistant", "content": response_content})
        self.current_attempts += 1
        self.logger.log(f"Model responded: {response_content}")
        return response_content

    def start(self):
        """Interactive CLI loop — user sends a footballer name, model replies, until STOP."""
        self.logger.log("=== Football Agent Started ===")
        self.logger.log("Type a footballer's name to begin. Type STOP to quit.\n")

        while True:
            try:
                # --- User turn ---
                user_input = input("You: ").strip()

                if not user_input:
                    self.logger.log("Empty input received, please enter a name.")
                    continue

                if user_input.upper() == "STOP":
                    self.logger.log("User issued STOP command. Ending session.")
                    break

                self.messages.append({"role": "user", "content": user_input})
                self.logger.log(f"User message appended: {user_input}")

                # --- Agent turn ---
                if self.current_attempts >= self.max_attempts:
                    self.logger.log(f"Max attempts ({self.max_attempts}) reached. Ending session.")
                    break

                response = self.attempt()

                if response.strip().upper() == "STOP":
                    self.logger.log("Model returned STOP. Ending session.")
                    break

                print(f"Agent: {response}\n")

            except KeyboardInterrupt:
                self.logger.log("\nKeyboardInterrupt received. Ending session gracefully.")
                break
            except Exception as e:
                self.logger.log(f"Error during turn: {type(e).__name__}: {e}")
                self.logger.log("Continuing to next turn...")
                continue

        self.logger.log("=== Football Agent Session Ended ===")
        self.logger.log(f"Total turns: {self.current_attempts}")
        self.logger.log(f"Total messages in history: {len(self.messages)}")