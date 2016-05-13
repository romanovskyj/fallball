from django.apps import AppConfig


class FallballAppConfig(AppConfig):
    name = 'fallballapp'

    def ready(self):
        from fallballapp import signals  # noqa
