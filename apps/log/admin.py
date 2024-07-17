import json

from django.contrib import admin
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer

from apps.core.adminmixins import AutoModelAdminMixin
from apps.log.models import AdminLog, ActionLog
from apps.utils.mixins.admin.core import NoAddAdminMixin


@admin.register(AdminLog)
class AdminLog(AutoModelAdminMixin, NoAddAdminMixin, admin.ModelAdmin):
    pass


@admin.register(ActionLog)
class ActionLogAdmin(AutoModelAdminMixin, NoAddAdminMixin, admin.ModelAdmin):

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(ActionLogAdmin, self).get_readonly_fields(request, obj))
        return readonly_fields + ['get_object_instance', ]

    def get_object_instance(self, obj):
        response = json.dumps(json.loads(obj.object_instance), sort_keys=True, indent=2)

        formatter = HtmlFormatter(style='colorful')
        response = highlight(response, JsonLexer(), formatter)

        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        return mark_safe(style + response)
