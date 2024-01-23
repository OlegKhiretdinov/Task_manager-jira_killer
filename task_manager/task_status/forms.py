from django.forms import ModelForm
from .models import TaskStatusModel


class TaskStatusCreateForm(ModelForm):
    class Meta:
        model = TaskStatusModel
        fields = ['name']
