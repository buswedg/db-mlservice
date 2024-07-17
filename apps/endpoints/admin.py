from django.apps import apps
from django.contrib import admin

from apps.core.adminmixins import AutoModelAdminMixin, AutoModelNoModuleAdminMixin

app_config = apps.get_app_config('endpoints')

app_config.model_imports()

no_module_models = ()

models = app_config.get_models()
for model in models:
    try:
        if model in no_module_models:
            admin.site.register(model, AutoModelNoModuleAdminMixin)
        else:
            admin.site.register(model, AutoModelAdminMixin)

    except admin.sites.AlreadyRegistered:
        pass
