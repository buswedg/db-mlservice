from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Site)
def post_save_site(sender, instance, created, **kwargs):
    for obj in instance.site_config.all():
        obj.save()
