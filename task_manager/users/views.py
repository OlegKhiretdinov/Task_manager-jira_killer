from django.shortcuts import render, redirect
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

        # return redirect('create_user')
        return render(request, 'users/create.html', {'form': form})
