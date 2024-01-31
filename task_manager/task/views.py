from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin

from .models import Task
from .forms import TaskCreateForm
from task_manager.utils import UnauthenticatedRedirectMixin, OnlOwnerAccessMixin


class IndexView(UnauthenticatedRedirectMixin, ListView):
    model = Task
    context_object_name = "tasks_list"
    template_name = 'task/index.html'


class CreateTaskView(UnauthenticatedRedirectMixin, SuccessMessageMixin, CreateView):
    form_class = TaskCreateForm
    template_name = "task/create.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("success_create_task_message")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTaskView(UnauthenticatedRedirectMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'executor', 'status']
    template_name = "task/update.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("success_update_task_message")


class DeleteTaskView(UnauthenticatedRedirectMixin, OnlOwnerAccessMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "task/delete.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("success_delete_task_message")
    context_object_name = "task"
    not_owner_redirect_path = "tasks_list"
    not_owner_error_message = _("error_only_owner_delete_task")

    def get_owner(self):
        return self.get_object().author


class ShowTaskView(UnauthenticatedRedirectMixin, DetailView):
    model = Task
    template_name = 'task/show.html'
