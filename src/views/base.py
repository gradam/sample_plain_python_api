import json


class View:
    login_required = False
    customer = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @staticmethod
    def response(data):
        return json.dumps(data).encode()
