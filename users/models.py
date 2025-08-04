from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
from datetime import timedelta


class User(AbstractUser):
    '''Модель пользователя'''
    email = models.EmailField(unique=True,
                              verbose_name='Адрес электронной почты',
                              blank=False,
                              null=False,
                              help_text='Обязательное поле')

    avatar = models.ImageField(upload_to='avatars/',
                               blank=True,
                               null=True,
                               verbose_name='Фото профиля',
                               help_text='Загрузите ваш аватар')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email


class ConfirmaionCode(models.Model):
    '''Модель создания кода для подтверждения регистрации'''
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='confirmation_codes')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @classmethod
    def generate_code(cls, user):
        cls.objects.filter(user=user).delete()

        code = str(random.randint(100000, 999999))
        return cls.objects.create(user=user, code=code)

    def is_valid(self):
        return self.is_active and (timezone.now() - self.created_at < timedelta(minutes=2))