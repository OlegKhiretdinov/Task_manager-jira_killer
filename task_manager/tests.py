from django.test import TestCase
from django.contrib.auth.models import User


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user1", "user1@mail.ru", "1234")

    def test_login(self):
        response = self.client.post("/login/", {'username': 'user1', 'password': '1234'}, follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Вы залогинены")


class UserLogoutTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user1", "user1@mail.ru", "1234")

    def test_logout(self):
        response = self.client.post("/logout/", follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Вы разлогинены")