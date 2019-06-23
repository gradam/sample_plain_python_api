import datetime as dt

from models.models import Plan
from utils.exceptions import DoesNotExistsError
from utils.payments import verify_payment
from views.base import View

from models.manager import Manager


class SubscribeView(View):
    login_required = True

    def post(self, data):
        if verify_payment(data["payment_token"]):
            plan_pk = data["plan"]
            try:
                Manager(Plan).get(pk=plan_pk)
            except DoesNotExistsError:
                return self.response({"error": "Plan does not exist"})

            self.customer.plan = plan_pk

            today = dt.date.today()
            ends = dt.date(year=today.year + 1, month=today.month, day=today.day)
            self.customer.subscription = ends.strftime("%Y/%m/%d")
            self.customer.save()
            return self.response({"success": "subscribed"})
        else:
            return self.response({"error": "payment failed"})
