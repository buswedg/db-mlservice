import uuid

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import striptags, truncatewords
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class TimestampMixin(models.Model):
    """
    Mixin that adds created_at and modified_at fields to a model.
    """
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('Modified at'), auto_now=True)

    class Meta:
        abstract = True


class AuthorMixin(models.Model):
    """
    Mixin that adds created_by and updated_by fields to a model.
    """
    created_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_created_by', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_updated_by', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if user:
            if not self.id:
                self.created_by = user
            else:
                self.updated_by = user
        super().save(*args, **kwargs)


class UuidMixin(models.Model):
    """
    Mixin that adds a uuid field to a model.
    """
    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, unique=True, editable=False)

    class Meta:
        abstract = True


class OrderMixin(models.Model):
    """
    Mixin that adds an order field to a model.
    """
    order = models.PositiveIntegerField(_('Order'), default=0)

    class Meta:
        abstract = True


class TitleMixin(models.Model):
    """
    Mixin that adds a title field to a model.
    """
    title = models.CharField(_('Title'), max_length=120, blank=True, null=True)

    class Meta:
        abstract = True


class TitleSlugMixin(models.Model):
    """
    Mixin that adds a title and slug field to a model.
    """
    title = models.CharField(_('Title'), max_length=120)
    slug = models.SlugField(_('Slug'), max_length=255, unique=True, editable=False, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class DescriptionMixin(models.Model):
    """
    Mixin that adds a description field to a model.
    """
    description = models.CharField(_('Description'), max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class FeaturedMixin(models.Model):
    """
    Mixin that adds a featured field to a model.
    """
    featured = models.BooleanField(_('Featured'), default=False)

    class Meta:
        abstract = True


class BodyMixin(models.Model):
    """
    Mixin that adds a body field to a model.
    """
    body = models.TextField(_('Body'), blank=True, null=True)

    class Meta:
        abstract = True


class PositionMixin(models.Model):
    """
    Mixin that adds a position field to a model.
    """
    POSITION_CHOICES = (
        ('top', 'top'),
        ('left', 'left'),
        ('right', 'right'),
        ('bottom', 'bottom'),
        ('center', 'center'),
        ('full', 'full')
    )

    position = models.CharField(_('Position'), max_length=10, choices=POSITION_CHOICES, default='center')

    class Meta:
        abstract = True


class BodyExcerptMixin(models.Model):
    """
    A mixin to automatically generate short and long excerpts from a `body` field.

    The `body` field is stripped of HTML tags and two new fields, `excerpt_short` and `excerpt_long`,
    are generated from the body text. `excerpt_short` contains the first 20 words of the body text and
    `excerpt_long` contains the first 40 words.

    To use this mixin, simply subclass this mixin and include it as a mixin in your Model class. When the `save` method
    is called, it will automatically generate and save the excerpts.
    """

    body = models.TextField(_('Body'), blank=True, null=True)
    excerpt_short = models.TextField(_('Excerpt short'), blank=True, null=True)
    excerpt_long = models.TextField(_('Excerpt long'), blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if self.body:
            body_raw = striptags(self.body)

            if not self.excerpt_short:
                self.excerpt_short = truncatewords(body_raw, 20)
            if not self.excerpt_long:
                self.excerpt_long = truncatewords(body_raw, 40)

        super().save(*args, **kwargs)


class SoftDeleteModelMixin(models.Model):
    """
    Mixin that adds a `deleted` field to a model and overrides the `delete()` method to set the `deleted` field to True
    """
    deleted = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    class Meta:
        abstract = True
