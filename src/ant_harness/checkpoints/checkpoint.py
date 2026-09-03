import os
import json
from datetime import datetime

class CheckPoint:
    def __init__(self, checkpoint_dir):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(self.checkpoint_dir, exist_ok=True)

    def save_checkpoint(self, checkpoint_data: dict):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checkpoint_path = os.path.join(self.checkpoint_dir, f"checkpoint_{timestamp}")
        os.makedirs(checkpoint_path, exist_ok=True)
        with open(os.path.join(checkpoint_path, "data.json"), "w") as f:
            json.dump(checkpoint_data, f)
        return checkpoint_path
    
    def load_checkpoint(self, checkpoint_path: str):
        with open(os.path.join(checkpoint_path, "data.json"), "r") as f:
            return json.load(f)