from django.apps import AppConfig

# from .functions.tweet import Tweet


class StoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "store"

    # def ready(self):
    #     Tweet()
