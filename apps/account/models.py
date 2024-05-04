from django.contrib.auth.models import Group, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from apps.log.modelmixins import ActionLogMixin
from apps.utils.mixins.models.atoms import TimestampMixin


class AccountGroup(Group):
    description = models.CharField(_('Description'), max_length=150, null=True, blank=True)

    def __str__(self):
        return self.name


class User(TimestampMixin, AbstractUser, ActionLogMixin):
    username_validator = UnicodeUsernameValidator()
    email_validator = EmailValidator()

    username = models.CharField(
        _('Username'),
        max_length=30,
        unique=True,
        help_text=_('Required. Please provide a valid username (3-30 characters, letters, digits and @/./+/-/_ only).'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(
        _('email'),
        max_length=75,
        unique=True,
        help_text=_('Required. Please provide a valid email address (max 75 characters).'),
        validators=[email_validator],
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    first_name = models.CharField(_('First name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True, null=True)
    pw_reset_on_login = models.BooleanField(_('Password reset on login'), default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ('email',)

    def __str__(self):
        return self.email

    def activate(self, save=True):
        self.is_active = True

        if save:
            self.save(**{'action_tag': 'activate'})

    def deactivate(self, save=True):
        self.is_active = False

        if save:
            self.save(**{'action_tag': 'deactivate'})

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}
