from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from task_manager.utils.test_utils import UnauthorizedTestMixin, get_message_txt


class TestSetUpMixin(UnauthorizedTestMixin):
    def setUp(self):
        self.user1 = User.objects.create_user("user1", "user1@mail.ru", "1234")
        self.user2 = User.objects.create_user("user2", "user2@mail.ru", "1234")

    # нельзя редактировать/удалять чужой профиль
    def check_not_owner_user_edit(self, response):
        self.assertEqual(response.redirect_chain[0], (reverse('users'), 302))
        self.assertEqual(get_message_txt(response), "У вас нет прав для изменения другого пользователя.")

    # успешное действия с профилем
    def check_user_edit(self, response):
        self.assertEqual(response.redirect_chain[0], (reverse('users'), 302))


class CreateUserTestCase(TestCase):
    def test_create_user(self):
        response = self.client.post(
            reverse("create_user"),
            {
                'first_name': 'first_name',
                'last_name': 'second_name',
                'username': 'user1',
                'password1': 'qwer123$',
                'password2': 'qwer123$',
            },
            follow=True
        )
        self.assertEqual(response.redirect_chain[0], (reverse('login'), 302))
        self.assertEqual(get_message_txt(response), "Пользователь успешно зарегистрирован")


class DeleteUserTestCase(TestSetUpMixin):
    #  удаление не авторизованным пользователем
    def test_delete_user_not_authorized(self):
        response = self.client.post(reverse('delete_user', args=[self.user1.id]), follow=True)
        self.check_unauthorized_response(response)

    # удаление не владельцем профиля
    def test_delete_user_not_owner(self):
        self.client.login(username="user1", password="1234")
        response = self.client.post(reverse('delete_user', args=[self.user2.id]), follow=True)
        self.check_not_owner_user_edit(response)

    # удаление владельцем профиля
    def test_delete_user(self):
        self.client.login(username="user2", password="1234")
        response = self.client.post(reverse('delete_user', args=[self.user2.id]), follow=True)
        self.check_user_edit(response)
        self.assertEqual(get_message_txt(response), "Пользователь успешно удалён")


class UpdateUserTestCase(TestSetUpMixin):
    #  Изменение профиля не авторизованным пользователем
    def test_delete_user_not_authorized(self):
        response = self.client.post(reverse('update_user', args=[self.user2.id]), follow=True)
        self.check_unauthorized_response(response)

    # Изменение профиля не владельцем профиля
    def test_delete_user_not_owner(self):
        self.client.login(username="user1", password="1234")
        response = self.client.post(
            reverse('update_user', args=[self.user2.id]),
            {
                'first_name': 'first_name',
                'last_name': 'last_name',
                'username': 'user2',
            },
            follow=True
        )
        self.check_not_owner_user_edit(response)

    # Изменение профиля владельцем профиля
    def test_delete_user(self):
        self.client.login(username="user2", password="1234")
        response = self.client.post(
            reverse('update_user', args=[self.user2.id]),
            {
                'first_name': 'first_name',
                'last_name': 'last_name',
                'username': 'user2',
            },
            follow=True
        )
        self.check_user_edit(response)
        self.assertEqual(get_message_txt(response), "Пользователь успешно изменен")
