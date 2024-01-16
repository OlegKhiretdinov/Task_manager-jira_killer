from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.contrib import messages


class CustomLogoutView(LogoutView):
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, _("success_logout_message"))
        return response


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    next_page = 'home'
    success_message = _("success_login_message")
