import hashlib

from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ua_parser import user_agent_parser

from apps.utils.helpers.requests import get_or_create_request_session_key, get_request_remote_addr, \
    get_request_ua_string
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
        (1, 'Update'),
        (2, 'Create'),
        (3, 'Delete'),
    )

    objects = ActionLogManager()

    app_name = models.CharField(_('App name'), max_length=30, blank=True, null=True)
    model_name = models.CharField(_('Model name'), max_length=30, blank=True, null=True)
    object_id = models.PositiveIntegerField(_('Object ID'), blank=True, null=True)
    object_instance = models.JSONField(_('Object instance'))

    action_type = models.PositiveSmallIntegerField(_('Action type'), choices=ACTION_TYPE_CHOICES, default=1)
    action_tag = models.CharField(_('Action tag'), max_length=255, blank=True, null=True)
    comment = models.TextField(_('Comment'), blank=True, null=True)

    class Meta:
        verbose_name = "Action Log"
        verbose_name_plural = "Action Log"
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.id)


class VisitLogManager(models.Manager):

    def build(self, request, timestamp):
        visit_log = VisitLog(
            user=request.user if request.user.is_authenticated else None,
            session_key=get_or_create_request_session_key(request),
            timestamp=timestamp,
            path=request.path,
            remote_addr=get_request_remote_addr(request),
            ua_string=get_request_ua_string(request),
        )

        visit_log.hash = visit_log.md5().hexdigest()

        return visit_log


class VisitLog(TimestampMixin, UuidMixin, models.Model):
    """
    Adapted from django-user-visit
    https://github.com/yunojuno/django-user-visit
    """

    objects = VisitLogManager()

    user = models.ForeignKey(
        get_user_model(),
        related_name='visit_log',
        verbose_name=_('User'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    session_key = models.CharField(_('Session key'), max_length=40)
    timestamp = models.DateTimeField(_('Timestamp'), default=timezone.now)
    path = models.CharField(_('Path'), max_length=2048, blank=True, null=True)
    remote_addr = models.CharField(_('Remote address'), max_length=100, blank=True, null=True)
    ua_string = models.TextField(_('UA string'), blank=True, null=True)
    hash = models.CharField(_('Hash'), max_length=32, unique=True)

    class Meta:
        verbose_name = "Visit Log"
        verbose_name_plural = "Visit Log"
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.hash = self.md5().hexdigest()
        super().save(*args, **kwargs)

    @property
    def parsed_ua(self):
        return user_agent_parser.Parse(self.ua_string)

    @property
    def date(self):
        return self.timestamp.date()

    def md5(self):
        hash = hashlib.md5(self.session_key.encode())

        hash.update(self.date.isoformat().encode())
        hash.update(self.path.encode())
        hash.update(self.remote_addr.encode())
        hash.update(self.ua_string.encode())

        return hash


class EmailLog(TimestampMixin, models.Model):
    from_email = models.EmailField(_('From email'), max_length=75, blank=True)
    recipients = models.TextField(_('Recipients'), blank=True, null=True)
    subject = models.CharField(_('Subject'), max_length=255, blank=True, null=True)
    body = models.TextField(_('Body'), blank=True, null=True)
    sent = models.BooleanField(_('Sent'), default=False)

    class Meta:
        verbose_name = "email Log"
        verbose_name_plural = "email Log"
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.id)
