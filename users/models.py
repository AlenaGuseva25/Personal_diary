import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Создает и сохраняет обычного пользователя с email и паролем"""
        if not email:
            raise ValueError('Пользователь должен иметь email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и сохраняет суперпользователя с email и паролем"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    '''Модель пользователя'''
    username = None
    email = models.EmailField(unique=True,
                              verbose_name='Адрес электронной почты',
                              blank=False,
                              null=False,
                              help_text='Обязательное поле')
    verification_token = models.UUIDField(editable=False, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def generate_verification_token(self):
        self.verification_token = uuid.uuid4()
        self.save()
        return self.verification_token

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
