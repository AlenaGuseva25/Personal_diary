from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from allauth.account.forms import ConfirmLoginCodeForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from users.forms import RegistrationForm
from users.models import ConfirmaionCode
from users.models import User

User = get_user_model()


class SingUpView(FormView):
    '''Регистрация пользователя '''
    template_name = 'users/signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('confirm')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        code = ConfirmaionCode.generate_code(user)
        send_mail(
            'Код подтверждения',
            f'Ваш код: {code.code}',
            None,
            [user.email],
            fail_silently=False,
        )
        self.request.session['user_email'] = user.email
        return super().form_valid(form)


class ConfirmCodeView(FormView):
    template_name = 'users/confirm_code.html'
    form_class = ConfirmLoginCodeForm
    success_url = reverse_lazy('diary-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = User.objects.get(email=self.request.session['user_email'])
        return kwargs

    def form_valid(self, form):
        user = User.objects.get(email=self.request.session['user_email'])
        login(self.request, user)
        ConfirmaionCode.objects.filter(user=user).update(is_active=False)
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('login')