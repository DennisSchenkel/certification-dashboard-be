from django.apps import AppConfig


class CertificationProcessConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "certification_process"

    def ready(self):
        import certification_process.signals
