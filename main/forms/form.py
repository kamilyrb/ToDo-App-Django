# -*- coding: utf-8 -*-
# from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    # captcha = CaptchaField()

    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #     if username and password:
    #         user = authenticate(username=username,password=password)
    #         if not user:
    #             raise forms.ValidationError('Kullanıcı adı veya şifreyi hatalı girdiniz!')
    #     return super(LoginForm,self).clean()
