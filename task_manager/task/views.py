from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from django_filters import FilterSet
from django_filters.filters import ModelChoiceFilter, BooleanFilter
from django.forms import CheckboxInput

from .models import Task
from .forms import TaskCreateForm
from task_manager.utils.mixins import UnauthenticatedRedirectMixin, OnlOwnerAccessMixin
from task_manager.label.models import LabelModel


class TaskFilterView(FilterSet):
    """
    фильтр задач
    поле labels заменено с мультиселекта на просто селект
    добавлен чекбокс 'только своои задачи'
    """
    label = ModelChoiceFilter(
        queryset=lambda query: LabelModel.objects.all(),
        label=_('Label'),
        field_name="labels"
    )

    self_tasks = BooleanFilter(
        method='get_user_task',
        label=_('only_your_own_tasks'),
        widget=CheckboxInput
    )

    def get_user_task(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(author=self.request.user)

    class Meta:
        model = Task
        fields = ['status', 'executor']


class IndexView(UnauthenticatedRedirectMixin, FilterView):
    model = Task
    context_object_name = "tasks_list"
    template_name = 'task/index.html'
    filterset_class = TaskFilterView


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
    fields = ['name', 'description', 'executor', 'status', 'labels']
    template_name = "task/update.html"
    success_url = reverse_lazy("tasks_list")
    success_message = _("success_update_task_message")


class DeleteTaskView(
    UnauthenticatedRedirectMixin,
    OnlOwnerAccessMixin,
    SuccessMessageMixin,
    DeleteView
):
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
