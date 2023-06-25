from django.apps import apps
from django.contrib import admin

from apps.utils.mixins.admin.core import AutoModelAdminMixin

app_config = apps.get_app_config('core')

app_config.model_imports()

models = app_config.get_models()
for model in models:
    try:
        admin.site.register(model, AutoModelAdminMixin)

    except admin.sites.AlreadyRegistered:
        pass
