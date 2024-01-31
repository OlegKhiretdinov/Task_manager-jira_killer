from django.db import models
from django.contrib.auth.models import User
from task_manager.task_status.models import TaskStatusModel


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+")
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+", blank=True, null=True)
    status = models.ForeignKey(TaskStatusModel, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
