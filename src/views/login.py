from uuid import uuid4

from views.base import View

from models.manager import Manager
from models.models import Customer, Token


class LoginView(View):
    def post(self, data):
        password = data.get("password", "")
        customer: Customer = Manager(Customer).get(email=self.kwargs["email"])
        if customer.verify_password(password):
            token = Token(customer=customer.pk, token=str(uuid4()))
            token.save()
            return self.response({"token": token.token})
        else:
            return self.response({"error": "Invalid password"})
