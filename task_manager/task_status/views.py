from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.task_status.models import TaskStatusModel
from task_manager.task_status.forms import TaskStatusCreateForm
from task_manager.utils.utils import UnauthenticatedRedirectMixin, DeleteProtectedEntityMixin


# список статусов
class IndexView(UnauthenticatedRedirectMixin, ListView):
    model = TaskStatusModel
    context_object_name = "statuses_list"
    template_name = 'statuses/index.html'


# создание статуса
class CreateTaskStatusView(UnauthenticatedRedirectMixin, SuccessMessageMixin, CreateView):
    form_class = TaskStatusCreateForm
    template_name = "statuses/create.html"
    success_url = reverse_lazy("statuses_list")
    success_message = _("success_create_status_message")


# обновления статуса
class UpdateTaskStatusView(UnauthenticatedRedirectMixin, SuccessMessageMixin, UpdateView):
    model = TaskStatusModel
    fields = ['name']
    template_name = "statuses/update.html"
    success_url = reverse_lazy("statuses_list")
    success_message = _("success_update_status_message")


# Удаления статуса
class DeleteTaskStatusView(UnauthenticatedRedirectMixin, SuccessMessageMixin, DeleteProtectedEntityMixin):
    model = TaskStatusModel
    template_name = "statuses/delete.html"
    success_url = reverse_lazy("statuses_list")
    success_message = _("success_delete_status_message")
    context_object_name = "status"
    delete_protected_error_pathname = "statuses_list"
    delete_protected_error_message = _("error_delete_used_status")
