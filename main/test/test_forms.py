from django.contrib.auth.models import User
from django.test import TestCase

from main.forms.form import UserForm, TodoForm


class UserFormTest(TestCase):
    def test_forms(self):
        form_data = {'username': 'test', 'password': '123', 'first_name': 'Name', 'last_name': 'Surname',
                     'email': 'abc@localhost.com', 'is_superuser': True}
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())


class UserCreateTestCase(TestCase):
    def setUp(self):
        username = 'test'
        password = '123'
        user = User.objects.create_user(username=username, password=password)


class TodoFormTest(UserCreateTestCase):
    def test_forms(self):
        user = User.objects.get(username='test')
        form_data = {'user': user.id, 'text': 'todo text', 'is_completed': False}
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())
