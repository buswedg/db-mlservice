from django.contrib import admin
from django_auto_admin.adminmixins import AutoModelBaseAdminMixin, AutoModelLinkAdminMixin

from apps.utils.mixins.admin.core import ExportCsvMixin, NoModuleAdminMixin


class AutoModelAdminMixin(AutoModelBaseAdminMixin, AutoModelLinkAdminMixin, ExportCsvMixin, admin.ModelAdmin):
    pass


class AutoModelNoModuleAdminMixin(AutoModelAdminMixin, NoModuleAdminMixin, ExportCsvMixin, admin.ModelAdmin):
    pass
