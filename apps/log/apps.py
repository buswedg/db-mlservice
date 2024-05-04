from django.apps import AppConfig


class LogConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    label = "log"
    name = "apps.log"

    @staticmethod
    def model_imports():
        import apps.log.models  # noqa

    @staticmethod
    def signal_imports():
        pass

    def ready(self):
        self.model_imports()
        self.signal_imports()