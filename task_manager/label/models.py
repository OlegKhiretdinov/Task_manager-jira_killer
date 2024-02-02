from django.db import models
from django.utils.translation import gettext as _


class LabelModel(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
