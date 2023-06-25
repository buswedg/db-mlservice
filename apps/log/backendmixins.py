from apps.log.models import EmailLog


class EmailLogBackendMixin(object):
    """
    A backend mixin to log emails.
    """

    def send_messages(self, email_messages):
        num_sent = 0

        for message in email_messages:
            recipients = ";".join(message.to)

            email = EmailLog.objects.create(
                from_email=message.from_email,
                recipients=recipients,
                subject=message.subject,
                body=message.body
            )

            num_sent += super().send_messages([message])

            if num_sent > 0:
                email.sent = True
                email.save()

        return num_sent
