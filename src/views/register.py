from views.base import View

from models.manager import Manager
from models.models import Customer


class RegisterView(View):
    def post(self, data):
        try:
            name = data["name"]
            password = data["password"]
            email = data["email"]
            subscription = None
            plan = None
        except KeyError:
            return self.response({"error": "Missing required data"})

        if any(Manager(Customer).filter(email=email)):
            return self.response({"error": "Email already in use"})

        customer = Customer(
            name=name,
            password=password,
            email=email,
            subscription=subscription,
            plan=plan,
        )
        customer.set_password(password)
        customer.save()

        return self.response({"uid": customer.pk})
