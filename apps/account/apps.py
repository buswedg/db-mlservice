from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    label = "account"
    name = "apps.account"

    @staticmethod
    def model_imports():
        import apps.account.models  # noqa

    @staticmethod
    def signal_imports():
        pass

    def ready(self):
        self.model_imports()
        self.signal_imports()