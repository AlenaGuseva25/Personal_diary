from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages


class ActiveUserMixin(UserPassesTestMixin):
    '''Миксин для проверки активного пользователя'''
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_active

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Ваш аккаунт не активирован')
        return super().handle_no_permission()
