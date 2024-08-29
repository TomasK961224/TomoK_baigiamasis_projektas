from django.apps import AppConfig


class AnimalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'animals'

    def ready(self):
        from .signals import create_profile, save_profile