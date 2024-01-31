from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Task
from task_manager.task_status.models import TaskStatusModel


class TestSetUpMixin(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="1234")
        self.status = TaskStatusModel.objects.create(name="status")
        self.task = Task.objects.create(
            name="Task name",
            author=self.user,
            status=self.status,
        )

    def check_unauthorized_response(self, response):
        self.assertEqual(response.redirect_chain[0], (reverse('login'), 302))
        self.assertContains(response, "Вы не авторизованы! Пожалуйста, выполните вход.")


class TaskListTestCase(TestSetUpMixin):
    def test_unauthorized_get_list(self):
        response = self.client.get(reverse('tasks_list'), follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_get_list(self):
        self.client.login(username="user", password="1234")
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)


class CreateTaskTestCase(TestSetUpMixin):
    def test_unauthorized_create_status(self):
        response = self.client.post(
            reverse('create_task'),
            {
                'name': 'new task',
                'status': self.status.id,
                'description': 'Task description'
            },
            follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_create_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(
            reverse('create_task'),
            {
                'name': 'new task',
                'status': self.status.id,
                'description': 'Task description'
            },
            follow=True)
        print(response)
        self.assertEqual(response.redirect_chain[0], (reverse('tasks_list'), 302))
        self.assertContains(response, "Задача успешно создана")


class UpdateTaskTestCase(TestSetUpMixin):
    def test_unauthorized_update_status(self):
        response = self.client.post(
            reverse('update_task', args=[self.task.id]),
            {
                'name': 'Update task',
                'status': self.status.id,
                'description': 'Task description'
            },
            follow=True)

        self.check_unauthorized_response(response)

    def test_authorized_update_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(
            reverse('update_task', args=[self.task.id]),
            {
                'name': 'Update tas',
                'status': self.status.id,
                'description': 'Task description'
            },
            follow=True)

        self.assertEqual(response.redirect_chain[0], (reverse('tasks_list'), 302))
        self.assertContains(response, "Задача успешно изменена")


class DeleteTaskTestCase(TestSetUpMixin):
    def test_unauthorized_delete_status(self):
        response = self.client.post(reverse('delete_task', args=[self.task.id]), follow=True)

        self.check_unauthorized_response(response)

    def test_authorized_delete_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(reverse('delete_task', args=[self.task.id]), follow=True)

        self.assertEqual(response.redirect_chain[0], (reverse('tasks_list'), 302))
        self.assertContains(response, "Задача успешно удалена")


class ShowTaskTestCase(TestSetUpMixin):
    def test_unauthorized_show_task(self):
        response = self.client.get(reverse('show_task', args=[self.task.id]), follow=True)

        self.check_unauthorized_response(response)

    def test_authorized_show_task(self):
        response = self.client.get(reverse('show_task', args=[self.task.id]), follow=True)
        self.assertEqual(response.status_code, 200)
