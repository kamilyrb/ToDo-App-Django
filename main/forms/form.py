# -*- coding: utf-8 -*-
# from captcha.fields import CaptchaField
import os

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from main.models import Todo


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['date_joined', 'is_active']


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        exclude = ['created_time', 'last_updated']

