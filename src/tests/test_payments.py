from unittest import TestCase

from utils.payments import verify_payment


class TestPayments(TestCase):
    def test_verify_payment(self):
        self.assertTrue(verify_payment(""))
