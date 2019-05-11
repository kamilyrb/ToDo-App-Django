from django.contrib.auth.models import User
from django.test import TestCase

from main.models import Todo


class UserCreateTestCase(TestCase):
    def setUp(self):
        username = 'test'
        password = '123'
        user = User.objects.create_user(username=username, password=password)


class UserModelTest(UserCreateTestCase):
    def test_user_model(self):
        user = User.objects.get(username='test')
        user.first_name = 'New Name'
        user.save()
        user.delete()


class TodoModelTest(UserCreateTestCase):
    def test_todo_model(self):
        to_do = Todo.objects.create(user_id=User.objects.get(username='test').id, text='Test', is_completed=False)
        to_do.is_completed = True
        to_do.save()
        to_do.delete()
