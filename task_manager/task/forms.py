from django.forms import ModelForm
from .models import Task


class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
