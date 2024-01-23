from django.test import TestCase
from task_manager.task_status.models import TaskStatusModel
from django.contrib.auth.models import User


class TestSetUpMixin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("user", "user@mail.ru", "1234")
        self.status = TaskStatusModel.objects.create(name="status")

    #  Не авторизованным пользователям запрещены любые действия со статусами
    def check_unauthorized_response(self, response):
        self.assertEqual(response.redirect_chain[0][0], '/login/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Вы не авторизованы! Пожалуйста, выполните вход.")


# Список статусов
class TaskStatusListTestCase(TestSetUpMixin):
    def test_unauthorized_get_list(self):
        # У не авторизованных пользователей нет доступа к списку
        response = self.client.get("/statuses/", follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_get_list(self):
        self.client.login(username="user", password="1234")
        response = self.client.get("/statuses/")
        self.assertEqual(response.status_code, 200)


# Создание статуса
class TaskStatusCreateTestCase(TestSetUpMixin):
    def test_unauthorized_create_status(self):
        # Не авторизованные пользователи не могут создавать статусы
        response = self.client.post("/statuses/create/", {'name': 'status name'}, follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_create_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post("/statuses/create/", {'name': 'status name'}, follow=True)
        self.assertEqual(response.redirect_chain[0][0], "/statuses/")
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Статус успешно создан")


class TaskStatusUpdateTestCase(TestSetUpMixin):
    def test_unauthorized_create_status(self):
        # Не авторизованные пользователи не могут обновлять статусы
        response = self.client.post(f'/statuses/{self.status.id}/update/', {'name': 'status name'}, follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_create_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(f'/statuses/{self.status.id}/update/', {'name': 'new status name'}, follow=True)
        self.assertEqual(response.redirect_chain[0][0], "/statuses/")
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Статус успешно изменен")


class TaskStatusDeleteTestCase(TestSetUpMixin):
    def test_unauthorized_delete_status(self):
        # Не авторизованные пользователи не могут удалять статусы
        response = self.client.post(f'/statuses/{self.status.id}/update/', {'name': 'status name'}, follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_delete_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(f'/statuses/{self.status.id}/delete/', follow=True)
        self.assertEqual(response.redirect_chain[0][0], "/statuses/")
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertContains(response, "Статус успешно удалён")
