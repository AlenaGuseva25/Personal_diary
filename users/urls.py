from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import RegisterView, LoginView, LogoutView, VerifyEmailView, CustomPasswordResetConfirmView
from .forms import CustomPasswordResetForm, ChangePasswordForm

app_name = 'users'

urlpatterns = [
    # Регистрация/Авторизация
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='users:login'), name="logout"),
    path("verify/<uuid:token>/", VerifyEmailView.as_view(), name="verify-email"),

    # Сброс пароля
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name="users/password_reset.html",
            success_url=reverse_lazy("users:password_reset_done"),
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/password_reset_subject.txt",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]