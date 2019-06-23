import tempfile
import datetime as dt
from pathlib import Path
from unittest import TestCase

import settings
from models.base import BaseModel, Field
from models.manager import Manager
from models.models import Customer
from utils.exceptions import ImproperlyConfigurated, DoesNotExistsError
from utils.loader import loader


class TestBaseModel(TestCase):
    class TestModel(BaseModel):
        test_field = Field()

    def test_init_without_kwargs(self):
        self.assertRaises(ImproperlyConfigurated, self.TestModel)

    def test_valid_init(self):
        value = "test123"
        model = self.TestModel(test_field=value)
        self.assertEqual(value, model.test_field)
        self.assertIsInstance(model.pk, str)

    def test_valid_init_with_pk(self):
        value = "test123"
        pk = "15"
        model = self.TestModel(test_field=value, pk=pk)
        self.assertEqual(value, model.test_field)
        self.assertEqual(model.pk, pk)

    def test_get_fields(self):
        fields = {"test_field", "pk"}
        self.assertEqual(set(self.TestModel._get_fields()), fields)

    def test_save(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            settings.data_dir = Path(tmpdir)

            value = "test4321"
            model = self.TestModel(test_field=value)
            model.save()
            pk = model.pk
            loader.clear_cache()
            self.assertEqual(loader.data, {})
            loaded_model = Manager(self.TestModel).get(pk=pk)
            self.assertEqual(loaded_model.test_field, value)

    def test_delete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            settings.data_dir = Path(tmpdir)

            value = "test4321"
            model = self.TestModel(test_field=value)
            model.save()
            pk = model.pk
            model.delete()
            loader.clear_cache()
            self.assertEqual(loader.data, {})
            with self.assertRaises(DoesNotExistsError):
                Manager(self.TestModel).get(pk=pk)


class TestCustomerModel(TestCase):
    def setUp(self) -> None:
        self.customer = Customer(
            name="test", password="test", email="test", subscription=None, plan=None
        )

    def test_set_password(self):
        old_pass = self.customer.password
        self.customer.set_password("pass")
        self.assertNotEqual(self.customer.password, old_pass)
        self.customer.set_password("pass2")
        self.assertNotEqual(self.customer.password, "pass")

    def test_verify_password(self):
        password = "test123"
        self.customer.set_password(password)
        self.assertTrue(self.customer.verify_password(password))

    def test_has_valid_subscription_no_subscription(self):
        self.assertFalse(self.customer.has_valid_subscription())

    def test_has_valid_subscription_expired_subscription(self):
        yesterday = dt.datetime.now() - dt.timedelta(days=1)
        yesterday = yesterday.strftime("%Y/%m/%d")
        self.customer.subscription = yesterday
        self.assertFalse(self.customer.has_valid_subscription())

    def test_has_valid_subscription_valid(self):
        tomorrow = dt.datetime.now() + dt.timedelta(days=1)
        tomorrow = tomorrow.strftime("%Y/%m/%d")
        self.customer.subscription = tomorrow
        self.assertTrue(self.customer.has_valid_subscription())

    def test_has_valid_subscription_today(self):
        today = dt.datetime.today()
        today = today.strftime("%Y/%m/%d")
        self.customer.subscription = today
        self.assertTrue(self.customer.has_valid_subscription())
