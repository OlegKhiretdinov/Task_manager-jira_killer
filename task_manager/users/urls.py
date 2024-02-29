from django.urls import path
from rest_framework import routers
from task_manager.users import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='users'),
    path('create/', views.CreateUserView.as_view(), name='create_user'),
    path('<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete_user'),
    path('<int:pk>/update/', views.UpdateUserView.as_view(), name='update_user'),
]

#  DRF
userRouter = routers.DefaultRouter()
userRouter.register(r'', views.UsersListAPI)
