from django.db import models
from config.settings import AUTH_USER_MODEL


class DiaryEntry(models.Model):
    '''Модель записи'''
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    content = models.TextField(verbose_name='Содержание')
    picture = models.ImageField(blank=True,
                                null=True,
                                upload_to='diary_pictures/%Y/%m/%d/',
                                verbose_name='Изображение',
                                help_text='Прикрепите фото для вашей записи')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True ,verbose_name='Дата изменения')
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Личная запись'
        verbose_name_plural = 'Личные записи'

    def __str__(self):
        return f'{self.title} ({self.owner})'