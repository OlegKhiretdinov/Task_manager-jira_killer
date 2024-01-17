from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.users.forms import CreateUserForm
from task_manager.utils import UnauthenticatedRedirectMixin, only_owner_access_decorator


# Список пользователей
class IndexView(View):
    def get(self, request):
        users_list = User.objects.all()
        return render(request, 'users/index.html', {'users_list': users_list})


# Создание пользователя
class CreateUserView(View):
    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        return render(request, 'users/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, _("success_signup_message"))
            return redirect('login')

        return render(request, 'users/create.html', {'form': form})


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
        UpdateView
      ):
    model = User
    fields = ['first_name', 'last_name', 'username', ]
    template_name = "users/update.html"
    success_url = reverse_lazy("users")
    success_message = _("success_update_user_message")

