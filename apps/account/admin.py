from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.utils.mixins.admin.core import ExportCsvMixin


@admin.register(get_user_model())
class UserAdmin(DjangoUserAdmin, ExportCsvMixin):
    list_display = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
        'created_at',
        'modified_at',
    ]

    list_display_links = [
        'id',
    ]

    search_fields = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    ]

    fieldsets = (
        (
            None, {
                'fields': (
                    'id', 'email', 'username', 'password', 'last_login', 'created_at', 'modified_at',
                )
            }
        ),
        (
            'Personal info', {
                'fields': (
                    'first_name', 'last_name',
                )
            }
        ),
        (
            'Permissions', {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',
                )
            }
        ),
    )

    readonly_fields = [
        'id',
        'last_login',
        'created_at',
        'modified_at',
    ]

    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
    )

    ordering = ('email',)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = []
        return super().add_view(request)
