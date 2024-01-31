from django.urls import path
from ..task import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='tasks_list'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/update/', views.UpdateTaskView.as_view(), name='update_task'),
    path('<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete_task'),
    path('<int:pk>/', views.ShowTaskView.as_view(), name='show_task'),
]
