import json

from . import _handler


class FileHandler(
    _handler.BaseHandler,
):
    def __init__(
        self, 
        file_path,
    ):
        self.file_path = file_path
        

    def read_json(
        self,
    ):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
            
        except FileNotFoundError:
            print(
                f'File {self.file_path} not found',
            )
        except json.JSONDecodeError as e:
            print(
                f'Error decoding JSON from {self.file_path}: {e}',
            )

        return {}

    def write_secrets(
        self, 
        secrets_data,
    ):
        try:
            with open(self.file_path, 'w+') as file:
                for key, value in secrets_data.items():
                    file.write(f'{key}: {value}\n')
        except Exception as e:
            print(
                f'Error writing to {self.file_path}: {e}'
            )