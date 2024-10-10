# certification_process/apps.py

from django.apps import AppConfig


class CertificationProcessConfig(AppConfig):
    name = 'certification_process'

    def ready(self):
        import certification_process.signals
