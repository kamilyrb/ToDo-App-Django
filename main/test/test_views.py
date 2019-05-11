from django.contrib.auth.models import User
from django.test import SimpleTestCase
from django.test import TestCase
from django.urls import reverse


class LoginRequiredTest(SimpleTestCase):
    def test_login_required_views(self):
        # dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEquals(response.status_code, 302)

        # logout
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)

        # user
        response = self.client.get(reverse('user_list'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('user_form'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 302)

        # to_do
        response = self.client.get(reverse('todo_form'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('export_todo_list'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('import_todo_list'))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('complete_todo', args=[0]))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('delete_todo', args=[0]))
        self.assertEquals(response.status_code, 302)

        # statistic
        response = self.client.get(reverse('statistic'))
        self.assertEquals(response.status_code, 302)


class LoggedInTestCase(TestCase):

    def setUp(self):
        username = 'test'
        password = '123'
        user = User.objects.create_user(username=username, password=password)
        self.client.login(username=username, password=password)


class UserTestCase(LoggedInTestCase):
    def test_user(self):
        response = self.client.get(reverse('user_list'))
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('user_form'))
        self.assertEquals(response.status_code, 200)


class TodoTestCase(LoggedInTestCase):
    def test_to_do(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('todo_form'))
        self.assertEquals(response.status_code, 200)

        #
        # response = self.client.get(reverse('logout'))
        # self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('export_todo_list'))
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('import_todo_list'))
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('complete_todo', args=[0]))
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('delete_todo', args=[0]))
        self.assertEquals(response.status_code, 200)

        response = self.client.get(reverse('statistic'))
        self.assertEquals(response.status_code, 200)


class LogoutTestCase(LoggedInTestCase):
    def test_to_do(self):
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)
