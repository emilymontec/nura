import requests
import os
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
from django.core.mail.message import EmailMessage

class MailgunAPIBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.api_key = os.getenv('MAILGUN_API_KEY')
        self.domain = os.getenv('MAILGUN_DOMAIN')
        self.api_url = f"https://api.mailgun.net/v3/{self.domain}/messages"

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
            
        num_sent = 0
        for message in email_messages:
            try:
                data = {
                    "from": message.from_email or getattr(settings, 'DEFAULT_FROM_EMAIL'),
                    "to": message.to,
                    "subject": message.subject,
                    "text": message.body,
                }
                
                # If there are html alternatives
                if hasattr(message, 'alternatives'):
                    for alt in message.alternatives:
                        if alt[1] == 'text/html':
                            data["html"] = alt[0]
                            break

                response = requests.post(
                    self.api_url,
                    auth=("api", self.api_key),
                    data=data
                )
                
                if response.status_code == 200:
                    num_sent += 1
                else:
                    print(f"Mailgun Error: {response.status_code} - {response.text}")
                    if not self.fail_silently:
                        pass # Avoid crashing the authentication flow
            except Exception as e:
                print(f"Mailgun Exception: {e}")
                if not self.fail_silently:
                    pass # Avoid crashing the authentication flow
        return num_sent
