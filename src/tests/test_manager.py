import tempfile
from pathlib import Path
from unittest import TestCase

import settings
from models.base import BaseModel, Field
from models.manager import Manager
from utils.exceptions import DoesNotExistsError
from utils.loader import loader


class TestManager(TestCase):
    class TestModel(BaseModel):
        test_field = Field()

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        settings.data_dir = Path(self.tempdir.name)

    def tearDown(self) -> None:
        loader.clear_cache()
        self.tempdir.cleanup()

    def test_filter(self):
        self.TestModel(test_field="instance1").save()
        self.TestModel(test_field="instance2").save()
        self.TestModel(test_field="instance2").save()

        results = Manager(self.TestModel).filter(test_field="instance2")
        self.assertEqual(2, len(results))

        for x in results:
            self.assertIsInstance(x, self.TestModel)

    def test_get(self):
        self.TestModel(test_field="instance1").save()
        self.TestModel(test_field="instance2").save()

        result = Manager(self.TestModel).get(test_field="instance1")
        self.assertIsInstance(result, self.TestModel)
        self.assertEqual(result.test_field, "instance1")

    def test_get_does_not_exists(self):
        self.TestModel(test_field="instance1").save()
        with self.assertRaises(DoesNotExistsError):
            Manager(self.TestModel).get(test_field="bla")

    def test_by_pk(self):
        instance = self.TestModel(test_field="instance1")
        instance.save()
        result = Manager(self.TestModel).get(pk=instance.pk)
        self.assertEqual("instance1", result.test_field)

    def test_not_existing_pk(self):
        instance = self.TestModel(test_field="instance1")
        instance.save()
        with self.assertRaises(DoesNotExistsError):
            Manager(self.TestModel).get(pk=instance.pk + "l")
