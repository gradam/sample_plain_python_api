from uuid import uuid4
from pathlib import Path

from utils.exceptions import ImproperlyConfigurated
from utils.loader import loader


class Field:
    pass


class BaseModel:
    pk = Field()

    def __init__(self, **kwargs):
        kwargs.setdefault("pk", str(uuid4()))

        for field in self._get_fields():
            try:
                value = kwargs[field]
            except KeyError:
                raise ImproperlyConfigurated(f"Missing required kwarg: {field}")
            setattr(self, field, value)

    @classmethod
    def _get_fields(cls):
        fields = []
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, Field):
                fields.append(attr_name)
        return fields

    def save(self):
        data = self.get_data()
        data[self.pk] = self.instance_data()
        loader.save(self._file(), data)

    def delete(self):
        data = self.get_data()
        del data[self.pk]
        loader.save(self._file(), data)

    @classmethod
    def get_data(cls) -> dict:
        return loader.load(cls._file())

    @classmethod
    def _file(cls) -> Path:
        return Path(f"{cls.__name__}.json")

    def instance_data(self) -> dict:
        return {field: getattr(self, field) for field in self._get_fields()}
