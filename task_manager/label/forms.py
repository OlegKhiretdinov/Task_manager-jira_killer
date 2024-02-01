from django.forms import ModelForm
from .models import LabelModel


class LabelCreateForm(ModelForm):
    class Meta:
        model = LabelModel
        fields = ['name']
