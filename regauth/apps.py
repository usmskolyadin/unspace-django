from django.apps import AppConfig


class RegauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'regauth'

    def ready(self):
        import regauth.signals
