from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.edit import DeleteView
from django.db.models import ProtectedError
from abc import ABC, abstractmethod


class UnauthenticatedRedirectMixin(LoginRequiredMixin):
    """
    Редирект не аутентифицированных пользователей и вывод сообщения
    """
    login_url = reverse_lazy("login")
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("error_unauthenticated_user_message"))
        return super().dispatch(request, *args, **kwargs)


class OnlOwnerAccessMixin(ABC):
    """
    Доступ только для владельца
    Обязательно переопределить метод get_owner - возвращает владельца
    """
    not_owner_redirect_path = "home"
    not_owner_error_message = _("error_only_owner_access_message")

    @abstractmethod
    def get_owner(self):
        return None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.get_owner() != request.user:
            messages.error(request, self.not_owner_error_message)
            return redirect(self.not_owner_redirect_path)
        return super().dispatch(request, *args, **kwargs)


class DeleteProtectedEntityMixin(DeleteView):
    """
    Обработка ошибки при удалении связанных сущностей
    ForeignKey on_delete=models.PROTECT
    """
    delete_protected_error_pathname = "home"
    delete_protected_error_message = _("delete_protected_error_message")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, args, kwargs)
        except ProtectedError:
            messages.error(request, self.delete_protected_error_message)
            return redirect(reverse_lazy(self.delete_protected_error_pathname))
