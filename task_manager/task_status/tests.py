from task_manager.task_status.models import TaskStatusModel
from django.contrib.auth.models import User
from django.urls import reverse

from task_manager.utils.test_utils import UnauthorizedTestMixin, get_message_txt


class TestSetUpMixin(UnauthorizedTestMixin):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="1234")
        self.status = TaskStatusModel.objects.create(name="status")

    # после любого успешного действия со статусами всегда редирект на страницу списка
    def check_success_status_redirect(self, response):
        self.assertEqual(response.redirect_chain[0], (reverse('statuses_list'), 302))


# Список статусов
class TaskStatusListTestCase(TestSetUpMixin):
    def test_unauthorized_get_list(self):
        # У не авторизованных пользователей нет доступа к списку
        response = self.client.get(reverse('statuses_list'), follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_get_list(self):
        self.client.login(username="user", password="1234")
        response = self.client.get(reverse('statuses_list'))
        self.assertEqual(response.status_code, 200)


# Создание статуса
class TaskStatusCreateTestCase(TestSetUpMixin):
    def test_unauthorized_create_status(self):
        # Не авторизованные пользователи не могут создавать статусы
        response = self.client.post(reverse('create_status'), {'name': 'status name'}, follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_create_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(reverse('create_status'), {'name': 'status name'}, follow=True)
        self.check_success_status_redirect(response)
        self.assertEqual(get_message_txt(response), "Статус успешно создан")


class TaskStatusUpdateTestCase(TestSetUpMixin):
    def test_unauthorized_create_status(self):
        # Не авторизованные пользователи не могут обновлять статусы
        response = self.client.post(
            reverse('update_status', args=[self.status.id]),
            {'name': 'status name'},
            follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_create_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(
            reverse('update_status', args=[self.status.id]),
            {'name': 'new status name'},
            follow=True)
        self.check_success_status_redirect(response)
        self.assertEqual(get_message_txt(response), "Статус успешно изменен")


class TaskStatusDeleteTestCase(TestSetUpMixin):
    def test_unauthorized_delete_status(self):
        # Не авторизованные пользователи не могут удалять статусы
        response = self.client.post(
            reverse('delete_status', args=[self.status.id]),
            {'name': 'status name'},
            follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_delete_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(
            reverse('delete_status', args=[self.status.id]),
            follow=True)
        self.check_success_status_redirect(response)
        self.assertEqual(get_message_txt(response), "Статус успешно удален")
