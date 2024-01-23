from django.urls import path
from task_manager.task_status import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='statuses_list'),
    path('create/', views.CreateTaskStatusView.as_view(), name='create_status'),
    path('<int:pk>/update/', views.UpdateTaskStatusView.as_view(), name='update_status'),
    path('<int:pk>/delete/', views.DeleteTaskStatusView.as_view(), name='delete_status'),
]
