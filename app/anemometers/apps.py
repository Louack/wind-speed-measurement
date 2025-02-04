from django.apps import AppConfig


class AnemometersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "anemometers"

    def ready(self):
        import anemometers.signals
