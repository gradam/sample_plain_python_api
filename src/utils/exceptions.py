class MyException(Exception):
    pass


class ImproperlyConfigurated(MyException):
    pass


class DoesNotExistsError(MyException):
    pass


class UnauthenticatedError(MyException):
    pass
