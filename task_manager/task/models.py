from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from task_manager.task_status.models import TaskStatusModel
from task_manager.label.models import LabelModel


class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    description = models.TextField(verbose_name=_('description'))
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+", verbose_name=_('author'))
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+", blank=True, null=True, verbose_name=_('executor'))
    status = models.ForeignKey(TaskStatusModel, on_delete=models.PROTECT, verbose_name=_('status'))
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(
        LabelModel,
        through='TaskLabelRelation',
        through_fields=('task', 'label'),
        blank=True,
        verbose_name=_('Labels'),
    )

    def __str__(self):
        return self.name


class TaskLabelRelation(models.Model):
    """
    запрет на удаление метки если связана с задачей
    """
    label = models.ForeignKey(LabelModel, on_delete=models.PROTECT)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
