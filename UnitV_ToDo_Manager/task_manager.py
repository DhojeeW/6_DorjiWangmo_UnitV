import json
from pathlib import Path


class TaskStorage:

    def __init__(self):
        # Create the data file in the project folder
        self.file_path = Path(__file__).with_name("tasks.json")

    # Load saved tasks
    def load_tasks(self):

        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            return []

    # Save tasks
    def save_tasks(self, tasks):

        with open(self.file_path, "w") as file:
            json.dump(tasks, file, indent=4)