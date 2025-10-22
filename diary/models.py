from django.db import models
from django.conf import settings


class DiaryEntry(models.Model):
    '''Модель записи'''
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True ,verbose_name='Дата изменения')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Личная запись'
        verbose_name_plural = 'Личные записи'

    def __str__(self):
        return f'{self.title} ({self.author})'