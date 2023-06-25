import csv

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.db.models import DateField, DateTimeField, ForeignKey, BooleanField, CharField, IntegerField, \
    SmallIntegerField, PositiveSmallIntegerField, PositiveIntegerField
from django.http import HttpResponse
from django.shortcuts import resolve_url
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import SafeText


def parse_field_config(links_config):
    """
    Returns a list of tuples with the model field name and the corresponding admin field name.
    """
    for link in links_config:
        model_field_name = link
        admin_field_name = '{}_link'.format(link)
        yield model_field_name, admin_field_name


def get_link_field(url, label):
    """
    Returns an HTML link with the given URL and label.
    """
    return format_html('<a href="{}" class="changelink">{}</a>', url, label)


def get_obj_link_field(obj, name):
    """
    Returns an HTML link to the change view of the given object.
    """
    url = resolve_url(admin_urlname(obj._meta, SafeText('change')), obj.pk)
    return get_link_field(url, name)


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


class AutoModelBaseAdminMixin(admin.ModelAdmin):
    """
    A mixin class that automatically generates some default admin options based on the fields in the model.

    The following options are generated:

    * list_display: a tuple of field names that will be displayed in the changelist view
    * list_filter: a tuple of field names that will be displayed as filters in the changelist view
    * search_fields: a tuple of field names that will be searched for in the changelist view
    * readonly_fields: a tuple of field names that will be read-only in the change view
    * ckeditor_fields: a tuple of field names that will use CKEditor in the change view
    * codemirror_fields: a tuple of field names that will use CodeMirror in the change view
    * date_hierarchy: the name of a field that will be used as the date hierarchy in the changelist view

    The options are generated based on the following criteria:

    * list_display: includes all non-relational fields that are not primary keys, up to a threshold of 10
    * list_filter: includes all non-relational fields that are of the following types: DateField, DateTimeField,
      ForeignKey, BooleanField, up to a threshold of 10
    * search_fields: includes the fields 'name', 'slug', and 'title'
    * readonly_fields: includes no fields by default, but can be manually set
    * ckeditor_fields: includes no fields by default, but can be manually set
    * codemirror_fields: includes the field 'body' by default, but can be manually set
    * date_hierarchy: includes the first field that matches the following names: 'joined_at', 'updated_at',
      'created_at', 'modified_at'

    To use this mixin, simply subclass it and include it as a mixin in your ModelAdmin class.
    """

    def __init__(self, model, admin_site):
        self.list_display = ()
        self.list_filter = ()
        self.search_fields = ()
        self.readonly_fields = ()
        self.ckeditor_fields = ()
        self.codemirror_fields = ()
        self.date_hierarchy = None

        self.set_list_display_fields(model)
        self.set_list_filter_fields(model)
        self.set_search_fields(model)
        self.set_codemirror_fields(model)
        self.set_date_hierarchy(model)

        super().__init__(model, admin_site)

    def set_list_display_fields(self, model):
        max_fields = 10
        display_field_types = (
            DateField,
            DateTimeField,
            ForeignKey,
            BooleanField,
            CharField,
            IntegerField,
            PositiveIntegerField,
            PositiveSmallIntegerField,
            SmallIntegerField,
        )

        fields = [f.name for f in model._meta.fields if not f.one_to_many and not f.one_to_one]
        for field in fields:
            if not self.list_display and model._meta.pk.name != field:
                self.list_display += (field,)
            elif isinstance(model._meta.get_field(field), display_field_types) and len(self.list_display) < max_fields:
                self.list_display += (field,)

    def set_list_filter_fields(self, model):
        max_fields = 10
        filter_field_types = (
            DateField,
            DateTimeField,
            ForeignKey,
            BooleanField,
        )

        fields = [f.name for f in model._meta.fields if not f.one_to_many and not f.one_to_one]
        for field in fields:
            if isinstance(model._meta.get_field(field), filter_field_types) and len(self.list_filter) < max_fields:
                self.list_filter += (field,)

    def set_search_fields(self, model):
        search_field_names = ['name', 'slug', 'title']
        fields = [f.name for f in model._meta.fields if not f.one_to_many and not f.one_to_one]
        self.search_fields = tuple(field for field in search_field_names if field in fields)

    def set_codemirror_fields(self, model):
        codemirror_field_names = ['body']
        fields = [f.name for f in model._meta.fields if not f.one_to_many and not f.one_to_one]
        self.codemirror_fields = tuple(field for field in codemirror_field_names if field in fields)

    def set_date_hierarchy(self, model):
        date_hierarchy_field_names = ['joined_at', 'updated_at', 'created_at', 'modified_at']
        fields = [f.name for f in model._meta.fields if not f.one_to_many and not f.one_to_one]
        for field in date_hierarchy_field_names:
            if field in fields and not self.date_hierarchy:
                self.date_hierarchy = field

                if field in self.list_display:
                    self.list_display = tuple(f for f in self.list_display if f != field) + (field,)


class AutoModelLinkAdminMixin(admin.ModelAdmin):
    """
    A mixin for Django admin models that adds links to related models in the change list and change views.

    Adapted from django-admin-relation-links
    https://github.com/gitaarik/django-admin-relation-links

    To use this mixin, simply subclass it and include it as a mixin in your ModelAdmin class.
    """

    def add_admin_field(self, field_name, func):
        if not hasattr(self, field_name):
            setattr(self, field_name, func)

        if field_name not in self.readonly_fields:
            self.readonly_fields += (field_name,)

    def add_change_link(self, model_field_name, admin_field_name):

        def make_change_link(model_field_name):
            def func(instance):
                return self.get_change_link(instance, model_field_name, admin_field_name)

            self.decorate_link_func(func, model_field_name)
            return func

        self.add_admin_field(admin_field_name, make_change_link(model_field_name))

    def get_change_link(self, instance, model_field_name, admin_field_name):
        try:
            target_instance = getattr(instance, model_field_name)
        except Exception:
            return

        return get_link_field(
            reverse(
                '{}:{}_{}_change'.format(
                    self.admin_site.name,
                    target_instance._meta.app_label,
                    target_instance._meta.model_name
                ),
                args=[target_instance.pk]
            ),
            self.link_label(admin_field_name, target_instance)
        )

    def add_changelist_link(self, model_field_name, admin_field_name):

        def make_changelist_link(model_field_name):
            def func(instance):
                return self.get_changelist_link(instance, model_field_name)

            self.decorate_link_func(func, model_field_name)
            return func

        self.add_admin_field(admin_field_name, make_changelist_link(model_field_name))

    def get_changelist_link(self, instance, model_field_name):
        try:
            target_instance = getattr(instance, model_field_name)
        except Exception:
            return

        if not target_instance.exists():
            return

        def get_url():
            return reverse(
                '{}:{}_{}_changelist'.format(
                    self.admin_site.name,
                    *self.get_app_model(instance, model_field_name)
                )
            )

        def get_lookup_filter():
            return instance._meta.get_field(model_field_name).field.name

        def get_label():
            return target_instance.model._meta.verbose_name_plural.capitalize()

        return get_link_field(
            '{}?{}={}'.format(get_url(), get_lookup_filter(), instance.pk), get_label()
        )

    def get_app_model(self, instance, model_field_name):
        model_meta = getattr(instance, model_field_name).model._meta
        app = model_meta.app_label
        model = model_meta.model_name

        return app, model

    def decorate_link_func(self, func, model_field_name):
        func.short_description = model_field_name.replace('_', ' ').capitalize()

        try:
            field = self.model._meta.get_field(model_field_name)
        except:
            pass
        else:
            if hasattr(field.related_model._meta, 'ordering') and len(field.related_model._meta.ordering) > 0:
                func.admin_order_field = '{}__{}'.format(
                    field.name,
                    field.related_model._meta.ordering[0].replace('-', '')
                )

    def link_label(self, admin_field_name, target_instance):
        label_method_name = '{}_label'.format(admin_field_name)
        if hasattr(self, label_method_name):
            return getattr(self, label_method_name)(target_instance)

        return str(target_instance)

    def __init__(self, model, admin_site):
        if not self.readonly_fields:
            self.readonly_fields = ()

        change_links = [
            f.name for f in model._meta.get_fields()
            if f not in model._meta.fields and f.one_to_one
        ]

        for model_field_name, admin_field_name in parse_field_config(change_links):
            self.add_change_link(model_field_name, admin_field_name)

        changelist_links = [
            f.name for f in model._meta.get_fields()
            if f not in model._meta.fields and f.one_to_many
        ]

        for model_field_name, admin_field_name in parse_field_config(changelist_links):
            self.add_changelist_link(model_field_name, admin_field_name)

        super().__init__(model, admin_site)


class AutoModelAdminMixin(AutoModelBaseAdminMixin, AutoModelLinkAdminMixin, ExportCsvMixin, admin.ModelAdmin):
    pass


class AutoModelNoModuleAdminMixin(AutoModelAdminMixin, NoModuleAdminMixin, ExportCsvMixin, admin.ModelAdmin):
    pass
