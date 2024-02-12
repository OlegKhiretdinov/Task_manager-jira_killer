from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.contrib.messages.views import SuccessMessageMixin

from .models import LabelModel
from .forms import LabelCreateForm
from task_manager.utils.mixins import UnauthenticatedRedirectMixin, DeleteProtectedEntityMixin


class IndexView(UnauthenticatedRedirectMixin, ListView):
    model = LabelModel
    context_object_name = "labels_list"
    template_name = 'label/index.html'


class CreateLabelView(UnauthenticatedRedirectMixin, SuccessMessageMixin, CreateView):
    form_class = LabelCreateForm
    template_name = "label/create.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("success_create_label_message")


class UpdateLabelView(UnauthenticatedRedirectMixin, SuccessMessageMixin, UpdateView):
    model = LabelModel
    fields = ['name']
    template_name = "label/update.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("success_update_label_message")


class DeleteLabelView(
    UnauthenticatedRedirectMixin,
    SuccessMessageMixin,
    DeleteProtectedEntityMixin
):
    model = LabelModel
    template_name = "label/delete.html"
    success_url = reverse_lazy("labels_list")
    success_message = _("success_delete_label_message")
    context_object_name = "label"
    delete_protected_error_pathname = "labels_list"
    delete_protected_error_message = _("error_delete_used_label")
