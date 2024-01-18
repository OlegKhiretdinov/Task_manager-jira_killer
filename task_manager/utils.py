from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect


class UnauthenticatedRedirectMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")
    redirect_field_name = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _("error_unauthenticated_user_message"))
        return super().dispatch(request, *args, **kwargs)


def only_owner_access_decorator(not_owner_redirect_url="/"):
    def wrapper(original_class):
        class DecoratedClass(original_class):
            def dispatch(self, request, *args, **kwargs):
                if request.user.is_authenticated and self.get_object() != request.user:
                    messages.error(request, _("error_only_owner_access_message"))
                    return redirect(not_owner_redirect_url)
                return super().dispatch(request, *args, **kwargs)

        return DecoratedClass
    return wrapper
