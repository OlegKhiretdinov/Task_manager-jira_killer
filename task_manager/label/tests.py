from django.urls import reverse

from task_manager.label.models import LabelModel
from django.contrib.auth.models import User
from task_manager.utils.test_utils import UnauthorizedTestMixin, get_message_txt


class TestSetUpMixin(UnauthorizedTestMixin):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="1234")
        self.label = LabelModel.objects.create(name="label")


class LabelsListTestCase(TestSetUpMixin):
    def test_unauthorized_get_list(self):
        response = self.client.get(reverse('labels_list'), follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_get_list(self):
        self.client.login(username="user", password="1234")
        response = self.client.get(reverse('labels_list'))
        self.assertEqual(response.status_code, 200)


class LabelCreateTestCase(TestSetUpMixin):
    def test_unauthorized_create_label(self):
        response = self.client.post(reverse('create_label'), {'name': 'label name'}, follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_create_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(reverse('create_label'), {'name': 'label name'}, follow=True)
        self.assertEqual(response.redirect_chain[0], (reverse('labels_list'), 302))
        self.assertEqual(get_message_txt(response), "Метка успешно создана")


class LabelUpdateTestCase(TestSetUpMixin):
    def test_unauthorized_create_status(self):
        response = self.client.post(
            reverse('update_label', args=[self.label.id]),
            {'name': 'New label name'},
            follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_create_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(
            reverse('update_label', args=[self.label.id]),
            {'name': 'New label name'},
            follow=True)
        self.assertEqual(response.redirect_chain[0], (reverse('labels_list'), 302))
        self.assertEqual(get_message_txt(response), "Метка успешно изменена")


class TaskStatusDeleteTestCase(TestSetUpMixin):
    def test_unauthorized_delete_label(self):
        response = self.client.post(reverse('delete_label', args=[self.label.id]), follow=True)
        self.check_unauthorized_response(response)

    def test_authorized_delete_status(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(reverse('delete_label', args=[self.label.id]), follow=True)
        self.assertEqual(response.redirect_chain[0], (reverse('labels_list'), 302))
        self.assertEqual(get_message_txt(response), "Метка успешно удалена")
