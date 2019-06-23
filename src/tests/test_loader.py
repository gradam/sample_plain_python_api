import json
import tempfile
import os
from pathlib import Path
from unittest import TestCase

import settings
from models.base import BaseModel, Field
from utils.loader import loader


class TestLoader(TestCase):
    class TestModel(BaseModel):
        test_field = Field()

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        settings.data_dir = Path(self.tempdir.name)

    def tearDown(self) -> None:
        loader.clear_cache()
        self.tempdir.cleanup()

    def test_clear_cache(self):
        loader.data[1] = 1
        loader.clear_cache()
        self.assertEqual({}, loader.data)

    def test_create_dir_if_not_exists(self):
        file_name = Path(self.tempdir.name) / "test" / "file.json"
        self.assertFalse(os.path.exists(file_name.parent))
        loader._create_dir_if_not_exists(file_name)
        self.assertTrue(os.path.exists(file_name.parent))

    def test_create_file_if_not_exists(self):
        file_name = Path(self.tempdir.name) / "test" / "file.json"
        self.assertFalse(os.path.exists(file_name))
        loader._create_file_if_not_exists(file_name)
        self.assertTrue(os.path.exists(file_name))

    def test_get_full_file_path(self):
        file_name = Path("file.json")
        self.assertEqual(
            Path(self.tempdir.name) / file_name, loader._get_full_file_path(file_name)
        )

    def test_save(self):
        data = {"test": "123"}
        file_name = Path("test.json")
        loader.save(file_name, data)
        file = Path(self.tempdir.name) / file_name
        self.assertTrue(os.path.exists(file))
        with file.open() as f:
            loaded_data = json.load(f)

        self.assertEqual(data, loaded_data)

    def test_load(self):
        data = {"test": "123"}
        file_name = Path("test.json")
        loader.save(file_name, data)
        loader.clear_cache()

        loaded_data = loader.load(file_name)
        self.assertEqual(loaded_data, data)
