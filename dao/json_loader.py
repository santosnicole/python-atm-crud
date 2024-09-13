import json

class JSONLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)
