import uuid

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import striptags, truncatewords
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ...helpers.django import get_processed_image_as_field_file, get_upload_path


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


class ResizeImageSaveMixin(models.Model):
    """
    Mixin that resizes an image field on save, creating new image fields in various sizes.

    Image processing is done with the 'get_processed_image_as_field_file' function. Resized images are stored in fields
    with names determined by the 'image_out_fields' dictionary. The original image field is determined by the 'image_in_field'
    attribute.

    The 'from_db' method is overridden to store the initial state of the model, which is used to compare if the image
    field has changed when the model is saved.

    To use this mixin, simply subclass this mixin and include it as a mixin in your Model class. The fields that are resized should
    be named according to the 'image_in_field' attribute, and the new fields will be named according to the 'image_out_fields'
    dictionary.
    """

    _stored: dict

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.image_in_field = "image"
        self.image_out_fields = {
            'image_xxs': {'size': [40, 30], 'force_format': 'WEBP', 'quality': 99},
            'image_xs': {'size': [160, 120], 'force_format': 'WEBP', 'quality': 99},
            'image_sm': {'size': [480, 360], 'force_format': 'WEBP', 'quality': 99},
            'image_md': {'size': [800, 600], 'force_format': 'WEBP', 'quality': 99},
            'image_lg': {'size': [1280, 960], 'force_format': 'WEBP', 'quality': 99},
            'image_xl': {'size': [1920, 1440], 'force_format': 'WEBP', 'quality': 99},
            'image_xxl': {'size': [2560, 1920], 'force_format': 'WEBP', 'quality': 99},
        }

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance._stored = dict(zip(field_names, values))

        return instance

    def save(self, *args, **kwargs):
        image_in = getattr(self, self.image_in_field, None)
        stored_image_in = self._stored.pop(self.image_in_field, None) if hasattr(self, '_stored') else None

        if image_in != stored_image_in:
            for field_name, image_kwargs in self.image_out_fields.items():
                if hasattr(self, field_name):
                    if image_in:
                        image_out = get_processed_image_as_field_file(image_in.file, image_in.name, **image_kwargs)
                    else:
                        image_out = None

                    setattr(self, field_name, image_out)

        super().save(*args, **kwargs)


class LogoSizeImageMixin(ResizeImageSaveMixin, models.Model):
    """
    A mixin for adding multiple versions of an image to a Django model for use as a logo.

    The following fields are added to the model:
        - image: the original image
        - image_xs: an extra small version of the image
        - image_md: a medium-sized version of the image
        - alt: the alternative text for the image

    The original image uploaded is resized to the dimensions specified in the image_xs and image_md fields using
    the ResizeImageSaveMixin class.

    To use this mixin, include it as a mixin in your model class and specify the image and alt text fields.
    """

    image = models.ImageField(_('Image'), upload_to=get_upload_path, max_length=255, blank=True, null=True)
    image_xs = models.ImageField(_('Image xs'), upload_to=get_upload_path, max_length=255, blank=True, null=True)
    image_md = models.ImageField(_('Image md'), upload_to=get_upload_path, max_length=255, blank=True, null=True)

    alt = models.CharField(_('Alt'), max_length=100, blank=True, null=True)

    class Meta:
        abstract = True


class CoverSizeImageMixin(ResizeImageSaveMixin, models.Model):
    """
    A mixin for adding multiple versions of an image to a Django model for use as a cover.

    The following fields are added to the model:
        - image: the original image
        - image_md: a medium-sized version of the image
        - image_xl: an extra large version of the image
        - alt: the alternative text for the image

    The original image uploaded is resized to the dimensions specified in the image_md and image_xl fields using
    the ResizeImageSaveMixin class.

    To use this mixin, simply subclass it and include it as a mixin in your model class.
    """

    image = models.ImageField(_('Image'), upload_to=get_upload_path, max_length=255, blank=True, null=True)
    image_md = models.ImageField(_('Image md'), upload_to=get_upload_path, max_length=255, blank=True, null=True)
    image_xl = models.ImageField(_('Image xl'), upload_to=get_upload_path, max_length=255, blank=True, null=True)

    alt = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True


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
