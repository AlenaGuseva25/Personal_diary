import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth.views import LogoutView as AuthLogoutView

from .forms import LoginForm, RegisterForm, CustomPasswordResetForm, ChangePasswordForm
from .models import User


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:register")

    def form_valid(self, form):
        user = form.save(commit=False)
        token = user.generate_verification_token()
        user.is_active = False
        user.save()

        verification_link = self.request.build_absolute_uri(
            f"/users/verify/{token}/"
        )
        send_mail(
            "Подтверждение регистрации в личном дневнике",
            f"Перейдите по ссылке для подтверждения: {verification_link}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        messages.success(
            self.request, "Письмо с подтверждением отправлено на вашу электронную почту"
        )
        return super().form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("diary:diary_list")

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, "Подтвердите ваш адрес электронной почты")
            return redirect("users:login")

        login(self.request, user)
        return super().form_valid(form)


class LogoutView(AuthLogoutView):
    next_page = reverse_lazy("users:login")


class VerifyEmailView(TemplateView):
    template_name = "users/verify_email.html"

    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            user.is_active = True
            user.verification_token = None
            user.save()
            messages.success(request, "Ваша электронная почта успешно подтверждена.")
            return redirect("users:login")
        except User.DoesNotExist:
            messages.error(request, "Недействительная ссылка подтверждения.")
            return redirect("users:register")


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "users/password_reset.html"
    success_url = reverse_lazy("users:password_reset_done")
    form_class = CustomPasswordResetForm
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"

    def form_valid(self, form):
        user = form.save(commit=False)
        token = user.generate_verification_token()

        verification_link = f"{settings.DOMAIN}/users/verify/{token}/"
        send_mail(
            "Восстановление пароля",
            f"Перейдите по ссылке для смены пароля: {verification_link}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        messages.success(
            self.request,
            "Письмо со ссылкой для смены пароля отправлено на вашу электронную почту",
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["domain"] = settings.DOMAIN
        context["protocol"] = "https" if self.request.is_secure() else "http"
        return context

@method_decorator(never_cache, name='dispatch')
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    "Установка нового пароля, сброс старого"

    form_class = ChangePasswordForm
    template_name = "users/registration/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")

    def form_valid(self, form):
        if form.errors:
            print("Ошибки формы:", form.errors)
            return self.form_invalid(form)
        with transaction.atomic():
            response = super().form_valid(form)
            update_session_auth_hash(self.request, self.request.user)
        messages.success(self.request, "Пароль успешно изменён")
        return response