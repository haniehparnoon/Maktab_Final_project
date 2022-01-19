from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import View


def superuser_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass
    return wrapper

def is_staff_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return self.request.user.is_staff and not (self.request.user.is_superuser)

        return WrappedClass
    return wrapper    

def customer_required():
    def wrapper(wrapped):
        class WrappedClass(UserPassesTestMixin, wrapped):
            def test_func(self):
                return not (self.request.user.is_staff) and not (self.request.user.is_superuser)

        return WrappedClass
    return wrapper 