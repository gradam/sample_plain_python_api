from utils.exceptions import DoesNotExistsError


class Manager:
    def __init__(self, obj):
        self.obj = obj

    def filter(self, **kwargs):
        data = []
        for entry in self.obj.get_data().values():
            if all(
                entry.get(field, None) == field_value
                for field, field_value in kwargs.items()
            ):
                data.append(self.obj(**entry))

        return data

    def get(self, pk=None, **kwargs):
        if pk is None:
            try:
                return self.filter(**kwargs)[0]
            except IndexError:
                raise DoesNotExistsError()
        else:
            try:
                data = self.obj.get_data()[pk]
                return self.obj(**data)
            except KeyError:
                raise DoesNotExistsError()
