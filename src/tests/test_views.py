import json
import tempfile
from pathlib import Path
from unittest import TestCase

import settings
from models.manager import Manager
from models.models import Customer, Token, Plan
from utils.loader import loader
from views.login import LoginView
from views.register import RegisterView
from views.subscribe import SubscribeView


class TestLoginView(TestCase):
    def setUp(self) -> None:
        self.customer = Customer(
            name="test", password="test", email="test", subscription=None, plan=None
        )
        self.tempdir = tempfile.TemporaryDirectory()
        settings.data_dir = Path(self.tempdir.name)

    def tearDown(self) -> None:
        loader.clear_cache()
        self.tempdir.cleanup()

    def test_login(self):
        password = "test"
        self.customer.set_password(password)
        self.customer.save()
        view = LoginView(email=self.customer.email)
        response = view.post({"password": password}).decode("utf-8")
        response = json.loads(response)
        self.assertTrue("token" in response)
        token = Manager(Token).get(token=response["token"])
        self.assertEqual(token.customer, self.customer.pk)

    def test_login_invalid_token(self):
        password = "test"
        self.customer.set_password(password)
        self.customer.save()
        view = LoginView(email=self.customer.email)
        response = view.post({"password": password + "1"}).decode("utf-8")
        response = json.loads(response)
        self.assertTrue("error" in response)


class TestRegisterView(TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        settings.data_dir = Path(self.tempdir.name)

    def tearDown(self) -> None:
        loader.clear_cache()
        self.tempdir.cleanup()

    def test_missing_data(self):
        view = RegisterView()
        response = view.post({}).decode("utf-8")
        response = json.loads(response)
        self.assertTrue("error" in response)

    def test_duplicated_email(self):
        email = "test"
        Customer(
            name="test", password="test", email=email, subscription=None, plan=None
        ).save()

        data = {"name": "name", "password": "name", "email": email}

        view = RegisterView()
        response = view.post(data).decode("utf-8")
        response = json.loads(response)

        self.assertTrue("error" in response)

    def test_success(self):
        data = {"name": "name", "password": "password", "email": "email"}

        view = RegisterView()
        response = view.post(data).decode("utf-8")
        response = json.loads(response)

        self.assertTrue("uid" in response)
        Manager(Customer).get(pk=response["uid"])


class TestSubscribeView(TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        settings.data_dir = Path(self.tempdir.name)
        self.customer = Customer(
            name="test", password="test", email="test", subscription=None, plan=None
        )
        self.plan = Plan(name='name', price='49.99', number_of_websites='3')
        self.plan.save()
        self.customer.save()

    def tearDown(self) -> None:
        loader.clear_cache()
        self.tempdir.cleanup()

    def test_plan_does_exists(self):
        view = SubscribeView()
        response = view.post({"plan": self.plan.pk + '1', "payment_token": ""}).decode("utf-8")
        response = json.loads(response)
        self.assertTrue('error' in response)

    def test_plan_success(self):
        view = SubscribeView()
        view.customer = self.customer
        response = view.post({"plan": self.plan.pk, "payment_token": ""}).decode("utf-8")
        response = json.loads(response)
        self.assertTrue('success' in response)
