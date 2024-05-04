from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.mixins.models.atoms import TimestampMixin, UuidMixin


class AdminLog(LogEntry):
    class Meta:
        proxy = True
        verbose_name = "Admin Log"
        verbose_name_plural = "Admin Log"


class ActionLogManager(models.Manager):

    def build(self, instance, **kwargs):
        content_type = ContentType.objects.get_for_model(instance)
        object_id = instance.id if hasattr(instance, 'id') else 0

        action_log = ActionLog(
            app_name=content_type.app_label,
            model_name=content_type.model,
            object_id=object_id,
            object_instance=serializers.serialize('json', [instance]),
            **kwargs
        )

        return action_log


class ActionLog(TimestampMixin, models.Model):
    ACTION_TYPE_CHOICES = (
        ('UP', _('Update')),
        ('CR', _('Create')),
        ('DE', _('Delete')),
    )

    objects = ActionLogManager()

    app_name = models.CharField(_('App name'), max_length=30, blank=True, null=True)
    model_name = models.CharField(_('Model name'), max_length=30, blank=True, null=True)
    object_id = models.PositiveIntegerField(_('Object ID'), blank=True, null=True)
    object_instance = models.JSONField(_('Object instance'))

    action_type = models.CharField(_('Action type'), choices=ACTION_TYPE_CHOICES, default=ACTION_TYPE_CHOICES[0][0], max_length=2)
    action_tag = models.CharField(_('Action tag'), max_length=255, blank=True, null=True)
    comment = models.TextField(_('Comment'), blank=True, null=True)

    class Meta:
        verbose_name = "Action Log"
        verbose_name_plural = "Action Log"
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.id)
