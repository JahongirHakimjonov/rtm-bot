from django.apps import AppConfig


class RtmConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.rtm"

    def ready(self):
        import apps.rtm.signals  # noqa
