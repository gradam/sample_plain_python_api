import hashlib
import binascii
import datetime as dt

from models.base import BaseModel, Field
from settings import secret_key


class Customer(BaseModel):
    name = Field()
    password = Field()
    email = Field()
    subscription = Field()
    plan = Field()

    def set_password(self, password):
        """Hash a password for storing."""
        pwdhash = hashlib.pbkdf2_hmac(
            "sha512", password.encode("utf-8"), secret_key.encode("ascii"), 100000
        )
        pwdhash = binascii.hexlify(pwdhash)
        self.password = pwdhash.decode("utf-8")

    def verify_password(self, provided_password):
        """Verify a stored password against one provided by user"""
        pwdhash = hashlib.pbkdf2_hmac(
            "sha512",
            provided_password.encode("utf-8"),
            secret_key.encode("ascii"),
            100000,
        )
        pwdhash = binascii.hexlify(pwdhash).decode("utf-8")
        return pwdhash == self.password

    def has_valid_subscription(self):
        if not self.subscription:
            return False
        valid_to = dt.datetime.strptime(self.subscription, "%Y/%m/%d")
        valid_to += dt.timedelta(hours=23, minutes=59, seconds=59)
        if valid_to <= dt.datetime.now():
            return False
        return True


class Plan(BaseModel):
    name = Field()
    price = Field()
    number_of_websites = Field()


class Website(BaseModel):
    url = Field()
    customer = Field()


class Token(BaseModel):
    customer = Field()
    token = Field()
