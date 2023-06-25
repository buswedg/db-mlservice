from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend
from django.core.mail.backends.smtp import EmailBackend as SmtpEmailBackend

from apps.log.backendmixins import EmailLogBackendMixin
from apps.utils.services.amazon_ses import AmazonSesHandler


class ConsoleEmailLogBackend(EmailLogBackendMixin, ConsoleEmailBackend):
    """
    A Django Email backend that uses the console to send emails, and logs them.
    """

    def send_messages(self, email_messages):
        return super().send_messages(email_messages)


class SmtpEmailLogBackend(EmailLogBackendMixin, SmtpEmailBackend):
    """
    A Django Email backend that uses SMTP to send emails, and logs them.
    """

    def send_messages(self, email_messages):
        return super().send_messages(email_messages)


class AmazonSesEmailLogBackend(EmailLogBackendMixin, BaseEmailBackend):
    """
    A Django Email backend that uses Amazon SES to send emails, and logs them.
    """

    def send_messages(self, email_messages):
        num_sent = 0

        amazon_ses = AmazonSesHandler()
        for message in email_messages:
            sent = amazon_ses.send_email(message)
            if sent:
                num_sent += 1

        return num_sent
