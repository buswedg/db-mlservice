from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    label = "core"
    name = "apps.core"

    @staticmethod
    def model_imports():
        pass

    @staticmethod
    def signal_imports():
        pass

    @staticmethod
    def task_imports():
        import apps.core.tasks  # noqa

    def ready(self):
        self.model_imports()
        self.signal_imports()
        self.task_imports()
