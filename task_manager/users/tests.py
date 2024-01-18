from django.test import TestCase
from django.contrib.auth.models import User


class UsersListTestCase(TestCase):
    pass


class CreateUserTestCase(TestCase):
    def test_create_user(self):
        response = self.client.post(
            "/users/create/",
            {
                'first_name': 'first_name',
                'last_name': 'second_name',
                'username': 'user1',
                'password1': 'qwer123$',
                'password2': 'qwer123$',
            },
            follow=True
        )
        self.assertEqual(response.redirect_chain[0][0], '/login/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Пользователь успешно зарегистрирован")


class DeleteUserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("user1", "user1@mail.ru", "1234")
        self.user2 = User.objects.create_user("user2", "user2@mail.ru", "1234")

    #  удаление не авторизованным пользователем
    def test_delete_user_not_authorized(self):
        response = self.client.post(f'/users/{self.user1.id}/delete/', follow=True)

        self.assertEqual(response.redirect_chain[0][0], '/login/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Вы не авторизованы! Пожалуйста, выполните вход.")

    # удаление не владельцем профиля
    def test_delete_user_not_owner(self):
        self.client.login(username="user1", password="1234")
        response = self.client.post(f'/users/{self.user2.id}/delete/', follow=True)

        self.assertEqual(response.redirect_chain[0][0], '/users/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "У вас нет прав для изменения другого пользователя.")

    # удаление владельцем профиля
    def test_delete_user(self):
        self.client.login(username="user2", password="1234")
        response = self.client.post(f'/users/{self.user2.id}/delete/', follow=True)
        self.assertEqual(response.redirect_chain[0][0], '/users/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Пользователь успешно удалён")


class UpdateUserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user("user1", "user1@mail.ru", "1234")
        self.user2 = User.objects.create_user("user2", "user2@mail.ru", "1234")

    #  Изменение профиля не авторизованным пользователем
    def test_delete_user_not_authorized(self):
        response = self.client.post(f'/users/{self.user1.id}/update/', follow=True)

        self.assertEqual(response.redirect_chain[0][0], '/login/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Вы не авторизованы! Пожалуйста, выполните вход.")

    # Изменение профиля не владельцем профиля
    def test_delete_user_not_owner(self):
        self.client.login(username="user1", password="1234")
        response = self.client.post(f'/users/{self.user2.id}/update/', follow=True)

        self.assertEqual(response.redirect_chain[0][0], '/users/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "У вас нет прав для изменения другого пользователя.")

    # Изменение профиля владельцем профиля
    def test_delete_user(self):
        self.client.login(username="user2", password="1234")
        response = self.client.post(
            f'/users/{self.user2.id}/update/',
            {
                'first_name': 'first_name',
                'last_name': 'last_name',
                'username': 'user2',
            },
            follow=True
        )
        self.assertEqual(response.redirect_chain[0][0], '/users/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Пользователь успешно изменен")