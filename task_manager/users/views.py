from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from rest_framework import viewsets, permissions
from task_manager.users.forms import CreateUserForm
from task_manager.utils.mixins import UnauthenticatedRedirectMixin, OnlOwnerAccessMixin, \
    DeleteProtectedEntityMixin
from task_manager.users.serializers import UserSerializer


User = get_user_model()


# Список пользователей
class IndexView(ListView):
    model = User
    context_object_name = "users_list"
    template_name = 'users/index.html'


class UsersListAPI(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.BasePermission]


# Создание пользователя
class CreateUserView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("login")
    success_message = _("success_signup_message")


# Удаление пользователя
class DeleteUserView(
    UnauthenticatedRedirectMixin,
    OnlOwnerAccessMixin,
    SuccessMessageMixin,
    DeleteProtectedEntityMixin
):
    model = User
    success_url = reverse_lazy("users")
    template_name = "users/delete.html"
    success_message = _("success_delete_user_message")
    delete_protected_error_pathname = "users"
    delete_protected_error_message = _("error_delete_used_user")
    not_owner_redirect_path = "users"
    not_owner_error_message = _("error_only_owner_edit_user")

    def get_owner(self):
        return self.get_object()


# Редактирование пользователей
class UpdateUserView(
        UnauthenticatedRedirectMixin,
        OnlOwnerAccessMixin,
        SuccessMessageMixin,
        UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username', ]
    template_name = "users/update.html"
    success_url = reverse_lazy("users")
    success_message = _("success_update_user_message")
    not_owner_redirect_path = "users"
    not_owner_error_message = _("error_only_owner_edit_user")

    def get_owner(self):
        return self.get_object()
