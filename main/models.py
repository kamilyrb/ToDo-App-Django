import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class USession(models.Model):
    id = models.IntegerField()
    first_name = models.CharField(
        max_length=100,
        verbose_name='Ad'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Soyad'
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name='Ad Soyad'
    )
    email = models.EmailField(
        max_length=100,
        verbose_name='Mail'
    )
    user_id = models.IntegerField(
        verbose_name='User ID'
    )

    def __str__(self):
        return self.full_name

    class Meta:
        abstract = True


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    text = models.CharField(max_length=255, verbose_name=_('Todo Text'))
    is_completed = models.BooleanField(default=False, verbose_name=_('Is Completed'))
    created_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name=_('Created Time'))
    last_updated = models.DateTimeField(default=datetime.datetime.now(), verbose_name=_('Last Updated'))
