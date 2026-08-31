from django.apps import AppConfig

class SmsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms_app'

    def ready(self):
        # Database seeding can be called after migrations
        pass
