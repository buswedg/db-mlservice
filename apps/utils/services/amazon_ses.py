import boto3
import logging
from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger('custom')


class AmazonSesHandler:
    """
    A module to handle Amazon SES API related operations.
    """

    def __init__(self, from_email=None):
        self.ses = boto3.client(
            'ses',
            aws_access_key_id=settings.AWS_SES_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SES_SECRET_ACCESS_KEY,
            region_name=settings.AWS_SES_REGION_NAME
        )
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL

    def send_email(self, message):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = message.subject
        msg['From'] = message.from_email
        msg['To'] = ', '.join(message.to)

        if message.cc:
            msg['Cc'] = ', '.join(message.cc)

        if message.reply_to:
            msg.add_header('reply-to', message.reply_to)

        text_part = MIMEText(message.body, 'plain')
        msg.attach(text_part)

        if message.alternatives:
            for alt in message.alternatives:
                if alt[1] == 'text/html':
                    html_part = MIMEText(alt[0], 'html')
                    msg.attach(html_part)

        try:
            response = self.ses.send_raw_email(
                Source=message.from_email,
                Destinations=message.to + message.cc + message.bcc,
                RawMessage={'Data': msg.as_string()}
            )

            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                return True

        except Exception as e:
            logger.error(f"Amazon SES Service: send_email error: {e}")

        return False
