from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages


def get_message_txt(response):
    messages = list(get_messages(response.wsgi_request))
    return str(messages[0])


class UnauthorizedTestMixin(TestCase):
    def check_unauthorized_response(self, response):
        self.assertEqual(response.redirect_chain[0], (reverse('login'), 302))
        self.assertEqual(
            get_message_txt(response),
            "Вы не авторизованы! Пожалуйста, выполните вход."
        )
