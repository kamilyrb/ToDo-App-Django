from django.test import SimpleTestCase
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

        response = self.client.get(reverse('complete_todo',args=[0]))
        self.assertEquals(response.status_code, 302)

        response = self.client.get(reverse('delete_todo',args=[0]))
        self.assertEquals(response.status_code, 302)

        # statistic
        response = self.client.get(reverse('statistic'))
        self.assertEquals(response.status_code, 302)


# class UsersPageTest(SimpleTestCase):
#
#
#     def test_users_page_status_code(self):
#         response = self.client.get(reverse('user_list'))
#         self.assertEquals(response.status_code, 302)
