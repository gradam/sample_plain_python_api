import json
import os
from pathlib import Path

import settings


class Loader:
    def __init__(self):
        self.data = {}

    def load(self, file_name: Path) -> dict:
        file_name = self._get_full_file_path(file_name)
        self._create_file_if_not_exists(file_name)
        if file_name in self.data:
            data = self.data[file_name]
        else:
            with file_name.open() as f:
                data = json.load(f)

        return data

    def save(self, file_name: Path, data: dict):
        file_name = self._get_full_file_path(file_name)
        with file_name.open("w") as f:
            json.dump(data, f)
        self.data[file_name] = data

    @staticmethod
    def _get_full_file_path(file_name: Path) -> Path:
        return settings.data_dir / file_name

    def _create_file_if_not_exists(self, file_name: Path):
        self._create_dir_if_not_exists(file_name)
        if not file_name.exists():
            with file_name.open("w") as f:
                json.dump({}, f)

    @staticmethod
    def _create_dir_if_not_exists(file_name: Path):
        os.makedirs(file_name.parent, exist_ok=True)

    def clear_cache(self):
        self.data = {}


loader = Loader()
