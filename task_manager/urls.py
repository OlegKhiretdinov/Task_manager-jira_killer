from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from task_manager.views import CustomLogoutView, CustomLoginView
from task_manager.users.urls import userRouter

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('statuses/', include('task_manager.task_status.urls')),
    path('tasks/', include('task_manager.task.urls')),
    path('labels/', include('task_manager.label.urls')),
    # DRF
    path('api/users/', include(userRouter.urls)),
]
