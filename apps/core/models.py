from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.mixins.models.atoms import TimestampMixin, TitleMixin


class SiteConfig(TimestampMixin, models.Model):
    site = models.ForeignKey(
        Site,
        related_name='site_config',
        verbose_name=_('Site'),
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(_('Is active?'), default=False)
    site_description = models.TextField(_('Site description'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Site Config"
        verbose_name_plural = "Site Config"

    def __str__(self):
        return self.site.name
