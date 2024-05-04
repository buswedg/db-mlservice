import csv

from django.contrib import admin
from django.http import HttpResponse


class NoAddAdminMixin(object):
    """
    Mixin to disable the add button in the admin.
    """

    extra = 0
    max_num = 0

    @staticmethod
    def has_add_permission(request, obj=None):
        return False


class NoDeleteAdminMixin(object):
    """
    Mixin to disable the delete button in the admin.
    """

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


class NoAddDeleteAdminMixin(NoAddAdminMixin):
    """
    Mixin to disable the add and delete buttons in the admin.
    """

    @staticmethod
    def has_delete_permission(request, obj=None):
        return False


class NoModuleAdminMixin(object):
    """
    Mixin to disable the module in the admin.
    """

    @staticmethod
    def has_module_permission(request, obj=None):
        return False


class ExportCsvMixin(admin.ModelAdmin):
    """
    This mixin allows you to export a csv file from the admin change list.
    """

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        if 'export_as_csv' not in self.actions:
            self.actions += ('export_as_csv',)

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"
