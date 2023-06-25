import json
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management import BaseCommand

from apps.core.models import SiteConfig


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('\n adding user model entries')

        superusers_path = os.path.join(settings.BASE_DIR, 'superusers.json')
        with open(superusers_path) as f:
            superusers = json.load(f)

        user_model = get_user_model()

        for superuser in superusers:
            username = superuser['username']

            if not user_model.objects.filter(username=username).exists():
                user_model.objects.create_superuser(**superuser)

        #######################################################################
        # site

        print('\n adding site')

        site = Site.objects.get(id=1)

        site.name = settings.DJANGO_SITE_NAME
        site.domain = settings.DJANGO_SITE_DOMAIN

        site.save()

        #######################################################################
        # configuration

        print('\n adding configuration')

        site_config = SiteConfig.objects.filter(site=site).last()

        if not site_config:
            site_config = SiteConfig.objects.create(site=site)

        site_config.site_description = """
Service to serve ML deployments
"""

        site_config.is_active = True

        site_config.save()
