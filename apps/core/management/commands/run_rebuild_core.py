import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from apps.utils.helpers.django import get_object_or_none


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('\n adding user model entries')

        superusers_path = os.path.join(settings.BASE_DIR, 'superusers.json')
        with open(superusers_path) as f:
            superusers = json.load(f)

        for superuser in superusers:
            username = superuser.get('username', 'user')
            email = superuser.get('email', 'user@domain.com')
            password = superuser.get('password', 'pass1234')

            user = get_object_or_none(get_user_model(), **{'username': username})
            if not user:
                user = get_user_model().objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )

            user.first_name = superuser.get('first_name', None)
            user.last_name = superuser.get('last_name', None)

            user.save()
