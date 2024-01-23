from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView

from task_manager.users.forms import CreateUserForm
from task_manager.utils import UnauthenticatedRedirectMixin, only_owner_access_decorator


# Список пользователей
class IndexView(ListView):
    model = User
    context_object_name = "users_list"
    template_name = 'users/index.html'


# Создание пользователя
class CreateUserView(SuccessMessageMixin, CreateView):
    form_class = CreateUserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("success_signup_message")


# Удаление пользователя
@only_owner_access_decorator("users")
class DeleteUserView(UnauthenticatedRedirectMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("users")
    template_name = "users/delete.html"
    success_message = _("success_delete_user_message")


# Редактирование пользователей
@only_owner_access_decorator("users")
class UpdateUserView(
        UnauthenticatedRedirectMixin,
        SuccessMessageMixin,
        UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', ]
    template_name = "users/update.html"
    success_url = reverse_lazy("users")
    success_message = _("success_update_user_message")
