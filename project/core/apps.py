from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        print("Starting delivery scheduler")
        from delivery_scheduler import letter_updater
        letter_updater.start()

