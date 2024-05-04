from django.apps import AppConfig


class MLConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    label = "ml"
    name = "apps.ml"

    @staticmethod
    def model_imports():
        pass

    @staticmethod
    def signal_imports():
        pass

    @staticmethod
    def registration_imports():
        import apps.ml.registration  # noqa

    def ready(self):
        self.model_imports()
        self.signal_imports()
        self.registration_imports()
