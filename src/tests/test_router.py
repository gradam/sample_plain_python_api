import tempfile
from pathlib import Path
from unittest import TestCase

import router
import settings
from models.models import Customer, Token
from utils.exceptions import UnauthenticatedError
from utils.loader import loader
from views.register import RegisterView
from views.website import WebsiteView


class TestGetView(TestCase):
    def test_get_view(self):
        self.assertIsInstance(router._get_view("/register"), RegisterView)

    def test_get_view_website(self):
        pk = "hejho_12"
        view = router._get_view(f"/website/{pk}")
        self.assertIsInstance(view, WebsiteView)
        self.assertEqual(pk, view.kwargs["pk"])


class TestRouter(TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        settings.data_dir = Path(self.tempdir.name)

    def tearDown(self) -> None:
        loader.clear_cache()
        self.tempdir.cleanup()

    def test_get_view(self):
        self.assertIsInstance(router.router("/register", ""), RegisterView)

    def test_login_required_view_without_token(self):
        path = "/website"
        with self.assertRaises(UnauthenticatedError):
            router.router(path, "")

    def test_login_required_view_with_token(self):
        path = "/website"
        customer = Customer(
            name="test", password="test", email="test", subscription=None, plan=None
        )
        customer.save()

        token_str = "token"
        token = Token(token=token_str, customer=customer.pk)
        token.save()

        view = router.router(path, token_str)
        self.assertIsInstance(view, WebsiteView)
        self.assertEqual(view.customer.pk, customer.pk)
