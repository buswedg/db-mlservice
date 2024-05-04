from django.apps import apps
from django.db import models


class ActionLogMixin(models.Model):
    action_fields = [
        'action_type',
        'action_tag',
        'comment'
    ]

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        action_kwargs = dict((k, kwargs.pop(k)) for k in self.action_fields if k in kwargs)
        super().save(*args, **kwargs)

        if action_kwargs:
            self.log_action(**action_kwargs)

    def delete(self, *args, **kwargs):
        action_kwargs = dict((k, kwargs.pop(k)) for k in self.action_fields if k in kwargs)
        super().delete(*args, **kwargs)

        if action_kwargs:
            action_kwargs.update({'action_type': 'DE'})
            self.log_action(**action_kwargs)

    def log_action(self, **kwargs):
        action_log_model = apps.get_model('common_log', 'ActionLog')
        action_log_model.objects.build(instance=self, **kwargs).save()
