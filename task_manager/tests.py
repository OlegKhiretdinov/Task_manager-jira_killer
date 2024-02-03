from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestSetUpMixin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", "user@mail.ru", "1234")


class UserLoginTestCase(TestSetUpMixin):
    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {
                'username': 'user',
                'password': '1234'
            },
            follow=True
        )
        self.assertEqual(response.redirect_chain[0], ('/', 302))
        self.assertContains(response, "Вы залогинены")


class UserLogoutTestCase(TestSetUpMixin):
    def test_logout(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(reverse("logout"), follow=True)
        self.assertEqual(response.redirect_chain[0], ('/', 302))
        self.assertContains(response, "Вы разлогинены")
