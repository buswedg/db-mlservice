from django.apps import AppConfig


class EndpointsConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    label = "endpoints"
    name = "apps.endpoints"

    @staticmethod
    def model_imports():
        import apps.endpoints.models  # noqa

    @staticmethod
    def signal_imports():
        pass

    def ready(self):
        self.model_imports()
        self.signal_imports()
