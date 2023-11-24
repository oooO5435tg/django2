from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from .utilities import get_timestamp_path
from django.contrib import admin


class User(AbstractUser):
   is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
   send_messages = models.BooleanField(default=False, verbose_name='Согласие на обработку персональных данных')
   last_name = models.CharField(max_length=200, blank=False, verbose_name='Фамилия')
   first_name = models.CharField(max_length=200, blank=False, verbose_name='Имя')
   patronymic = models.CharField(max_length=200, blank=False, verbose_name='Отчество')

   class Meta(AbstractUser.Meta):
       pass

   def delete(self, *args, **kwargs):
       for bb in self.bb_set.all():
           bb.delete()
       super().delete(*args, **kwargs)

#Проверка на соответствие идентификаторов авторизованного пользователя и автора текущего объявления
   def is_author(self, bb):
       if self.pk == bb.author.pk:
           return True
       return False
   class Meta(AbstractUser.Meta):
       pass

   def clean(self):
       if not self.send_messages:
           raise ValidationError('Необходимо дать согласие на обработку персональных данных')

class Category(models.Model):
    category_title = models.CharField(max_length=200, verbose_name='Название категории')

    def __str__(self):
        return self.category_title

class Request(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название заявки')
    content = models.TextField(verbose_name='Описание заявки')
    image = models.ImageField(blank=True, upload_to='image/', verbose_name='Фотография')
    image_design = models.ImageField(blank=True, upload_to='design/', verbose_name='Выберите фотографию')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Временная метка')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    choices = (
        ('Новая', 'Новая'),
        ('Принято в работу', 'Принято в работу'),
        ('Выполнено', 'Выполнено'),
    )
    status = models.CharField(verbose_name="Статус", max_length=200, choices=choices, default='Новая')
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=False)
    comment = models.TextField(blank=True)

    def is_completed(self):
        return self.status == 'Выполнено'

    def delete(self, *args, **kwargs):
       for ai in self.additionalimage_set.all():
           ai.delete()
       super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

class RequestAdmin(admin.ModelAdmin):
    list_display = ('category')

class AdditionalImage(models.Model):
    bb = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name='Заявка')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Фотография')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'