from models.manager import Manager
from models.models import Plan, Website
from views.base import View


class WebsiteView(View):
    login_required = True

    def post(self, data):
        if not self.customer.has_valid_subscription():
            return self.response({"error": "no valid subscription"})

        plan = Manager(Plan).get(pk=self.customer.plan)
        websites = Manager(Website).filter(customer=self.customer)

        if len(websites) >= int(plan.number_of_websites):
            return self.response({"error": "maximum number of websites for your plan"})

        if "url" not in data:
            return self.response({"error": "missing website url"})

        website = Website(url=data["url"], customer=self.customer.pk)
        website.save()
        return self.response({"website": website.pk})

    def patch(self, data):
        website = Manager(Website).get(pk=self.kwargs["pk"])

        if website.customer.pk != self.customer.pk:
            return self.response({"error": "Not allowed"})

        if "url" not in data:
            return self.response({"error": "missing website url"})

        website.url = data["url"]
        website.save()
        return self.response({"success": "website updated"})

    def delete(self):
        website = Manager(Website).get(pk=self.kwargs["pk"])

        if website.customer.pk != self.customer.pk:
            return self.response({"error": "Not allowed"})

        website.delete()

        return self.response({"deleted": "website deleted"})
