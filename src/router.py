import re

from models.manager import Manager
from models.models import Token, Customer
from utils.exceptions import DoesNotExistsError, UnauthenticatedError
from views.login import LoginView
from views.register import RegisterView
from views.subscribe import SubscribeView
from views.website import WebsiteView


def router(path: str, token):
    view = _get_view(path)
    if view.login_required:
        try:
            token = Manager(Token).get(token=token)
        except DoesNotExistsError:
            raise UnauthenticatedError()

        customer = Manager(Customer).get(pk=token.customer)
        view.customer = customer

    return view


def _get_view(path: str):
    match = re.match(r"^/login/(?P<email>.+)", path)
    if match:
        return LoginView(**match.groupdict())

    elif path == "/register":
        return RegisterView()

    elif path == "/subscribe":
        return SubscribeView()

    elif path == "/website":
        return WebsiteView()

    match = re.match(r"^/website/(?P<pk>.+)", path)
    if match:
        return WebsiteView(**match.groupdict())
