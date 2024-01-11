from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User

from task_manager.users.forms import CreateUserForm


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
            return redirect('users')

        return render(request, 'users/create.html', {'form': form})


# Удаление пользователя
class DeleteUserView(View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('pk'))
        return render(request, 'users/delete.html', {"full_user_name": user.get_full_name(), "id": user.id})

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get('pk'))
        user.delete()
        return redirect('users')