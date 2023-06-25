import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.core.models import SiteConfig

logger = logging.getLogger('custom')


def get_site_config_or_none():
    return SiteConfig.objects.filter(is_active=True).last()


def dispatch_email(email, email_type, email_data):
    site_config = get_site_config_or_none()
    if site_config:
        email_data.update({
            'site_name': site_config.site.name,
            'protocol': 'https' if settings.SECURE_SSL_REDIRECT else 'http',
            'domain': site_config.site.domain,
            'admin_email': settings.ADMIN_EMAIL,
            'social_link': site_config.social_link.all().values('type', 'social_url')
        })

        tpl_dir = f"core/emails/{email_type}"
        subject_tpl = "subject.txt"
        body_text_tpl = "body.txt"
        body_html_tpl = "body.html"

        subject = render_to_string(f'{tpl_dir}/{subject_tpl}', email_data)
        body_text = render_to_string(f'{tpl_dir}/{body_text_tpl}', email_data)
        body_html = render_to_string(f'{tpl_dir}/{body_html_tpl}', email_data)

        email = EmailMultiAlternatives(
            subject=subject,
            body=body_text,
            from_email=settings.ADMIN_EMAIL,
            to=[email],
            bcc=[settings.ADMIN_EMAIL]
        )

        email.attach_alternative(body_html, 'text/html')

        email.send()
