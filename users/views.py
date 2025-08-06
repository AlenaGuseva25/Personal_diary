from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib import messages
from allauth.account.forms import ConfirmLoginCodeForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LoginView, LogoutView

from users.forms import RegistrationForm, ConfirmationCodeForm
from users.models import ConfirmationCode
from users.models import User

User = get_user_model()


class Register(FormView):
    '''Регистрация пользователя с отправкой кода подтверждения'''
    template_name = 'users/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('confirm')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']

        user = User.objects.create_user(
            email=email,
            password=password,
            is_active=False
        )

        code = ConfirmationCode.generate_code(user)
        send_mail(
            'Код подтверждения для вашего дневника',
            f'Ваш код подтверждения: {code.code}\n\nКод действителен в течение 2 минут.',
            None,
            [user.email],
            fail_silently=False,
        )

        self.request.session['user_email'] = user.email
        self.request.session['register_time'] = str(timezone.now())

        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'


class ConfirmCodeView(FormView):
    template_name = 'users/confirm_code.html'
    form_class = ConfirmationCodeForm
    success_url = reverse_lazy('diary-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = User.objects.get(email=self.request.session['user_email'])
        return kwargs

    def form_valid(self, form):
        user = User.objects.get(email=self.request.session['user_email'])
        try:
            code_obj = ConfirmationCode.objects.get(
                user=user,
                code=form.cleaned_data['code'],
                is_active=True
            )
            if not code_obj.is_valid():
                form.add_error('code', 'Код устарел')
                return self.form_invalid(form)

            user.is_active = True
            user.save()
            code_obj.is_active = False
            code_obj.save()
            login(self.request, user)

            if 'user_email' in self.request.session:
                del self.request.session['user_email']
            if 'confirm_attempts' in self.request.session:
                del self.request.session['confirm_attempts']

            messages.success(self.request, 'Email успешно подтвержден!')
            return super().form_valid(form)

        except ConfirmationCode.DoesNotExist:
            form.add_error('code', 'Неверный код')
            return self.form_invalid(form)


class ResendCodeView(FormView):
    '''Повторная отправка кода ХХХХХХ'''
    template_name = 'users/resend_code.html'
    form_class = ConfirmationCodeForm

    def get(self, request):
        if 'user_email'not in self.request.session:
            return redirect('register')

        user = User.objects.get(email=self.request.session['user_email'])
        code = ConfirmationCode.generate_code(user)

        send_mail(
            'Новый код подтверждения',
            f'Ваш новый код: {code.code}\n\nКод действителен в течение 2 минут.',
            None,
            [user.email],
            fail_silently=False,
        )

        messages.success(request, 'Новый код отправлен на вашу почту')
        return redirect('confirm')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_email.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('login')