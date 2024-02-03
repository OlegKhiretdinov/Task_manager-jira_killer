from django.contrib.auth import get_user_model

User = get_user_model()


def user_full_name(self):
    return self.get_full_name()


User.__str__ = user_full_name
