from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm as BasePasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import ConfirmationCode

User = get_user_model()

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        return email

    def clean_password(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

class SignUpForm(forms.Form):
    email = forms.EmailField()

class ConfirmationCodeForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'XXXXXX'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            confirm_code = ConfirmationCode.objects.get(
                user=self.user,
                code=code,
                is_active=True
            )
            if not confirm_code.is_valid():
                raise ValidationError('Код устарел (действителен только 2 минуты)')
            return code
        except ConfirmationCode.DoesNotExist:
            raise ValidationError('Неверный код подтверждения')

class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

class NewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Подтвердите пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )