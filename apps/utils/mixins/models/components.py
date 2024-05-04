from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .atoms import OrderMixin, FeaturedMixin, TitleMixin, TitleSlugMixin, BodyMixin, \
    BodyExcerptMixin, CoverSizeImageMixin, DescriptionMixin, PositionMixin


class PageMixin(DescriptionMixin, models.Model):
    """
    Mixin that adds a description field to a model.
    """
    summary = models.TextField(_('Summary'), blank=True, null=True)

    class Meta:
        abstract = True


class HeaderMixin(TitleMixin, BodyMixin, models.Model):
    """
    Mixin that adds a title and body field to a model.
    """
    class Meta:
        abstract = True


class HeroMixin(TitleMixin, BodyMixin, PositionMixin, models.Model):
    """
    Mixin that adds a title, body and position selector field to a model.
    """
    class Meta:
        abstract = True


class HeroImageMixin(HeroMixin, CoverSizeImageMixin, models.Model):
    """
    Mixin that adds a title, cover image, body and position selector field to a model.
    """
    class Meta:
        abstract = True


class ContentMixin(OrderMixin, TitleMixin, BodyMixin, PositionMixin, models.Model):
    """
    Mixin that adds an order, title, body and position selector field to a model.
    """
    class Meta:
        abstract = True


class ContentImageMixin(ContentMixin, CoverSizeImageMixin, models.Model):
    """
    Mixin that adds an order, title, cover image, body and position selector field to a model.
    """
    class Meta:
        abstract = True


class CarouselMixin(OrderMixin, TitleMixin, CoverSizeImageMixin, models.Model):
    """
    Mixin that adds an order, title and cover image field to a model.
    """
    class Meta:
        abstract = True


class FeatureMixin(OrderMixin, TitleMixin, BodyMixin, models.Model):
    """
    Mixin that adds an order, title and body field to a model.
    """
    class Meta:
        abstract = True


class RecordMixin(OrderMixin, TitleSlugMixin, models.Model):
    """
    Mixin that adds an order, title and slug field to a model.
    """
    class Meta:
        abstract = True


class DocumentMixin(TitleMixin, BodyMixin, FeaturedMixin, models.Model):
    """
    Mixin that adds a title, body, featured, datetime and published field to a model.
    """
    datetime = models.DateTimeField(_('Datetime'), default=timezone.now, editable=True)
    published = models.BooleanField(_('Published'), default=False)

    class Meta:
        abstract = True


class PostMixin(TitleSlugMixin, BodyExcerptMixin, FeaturedMixin, models.Model):
    """
    Mixin that adds a title, slug, body, excerpt, featured, datetime and published field to a model.
    """
    datetime = models.DateTimeField(_('Datetime'), default=timezone.now, editable=True)
    published = models.BooleanField(_('Published'), default=False)

    class Meta:
        abstract = True
