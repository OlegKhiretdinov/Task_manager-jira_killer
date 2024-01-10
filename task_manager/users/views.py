from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User


class IndexView(View):

    def get(self, request):
        users_list = User.objects.all()

        return render(request, 'users/index.html', context={'users_list': users_list})
