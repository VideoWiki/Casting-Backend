from django.apps import AppConfig


class BbbApiConfig(AppConfig):
    name = 'bbb_api'

class UserMailConfig(AppConfig):
    name = 'bbb_api'

    def ready(self):
        import bbb_api.signals
