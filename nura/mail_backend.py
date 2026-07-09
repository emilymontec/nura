import requests
import os
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

class MailgunAPIBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.api_key = os.getenv('MAILGUN_API_KEY')
        self.domain = os.getenv('MAILGUN_DOMAIN')
        self.api_url = f"https://api.mailgun.net/v3/{self.domain}/messages"
        self.default_from = getattr(settings, 'DEFAULT_FROM_EMAIL', None)

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        num_sent = 0
        
        # Check if we have necessary credentials
        if not self.api_key or not self.domain:
            print("Mailgun Error: Missing MAILGUN_API_KEY or MAILGUN_DOMAIN environment variables")
            if not self.fail_silently:
                return 0
            
        for message in email_messages:
            try:
                # Prepare from email
                from_email = message.from_email or self.default_from
                if not from_email:
                    print("Mailgun Error: No from email address available")
                    continue
                
                data = {
                    "from": from_email,
                    "to": message.to,
                    "subject": message.subject,
                    "text": message.body,
                }
                
                # Handle cc and bcc if present
                if hasattr(message, 'cc') and message.cc:
                    data["cc"] = message.cc
                if hasattr(message, 'bcc') and message.bcc:
                    data["bcc"] = message.bcc
                
                # If there are html alternatives
                if hasattr(message, 'alternatives') and message.alternatives:
                    for alt in message.alternatives:
                        if len(alt) >= 2 and alt[1] == 'text/html':
                            data["html"] = alt[0]
                            break

                print(f"Sending email via Mailgun to {message.to}...")
                response = requests.post(
                    self.api_url,
                    auth=("api", self.api_key),
                    data=data,
                    timeout=30
                )
                
                print(f"Mailgun response status: {response.status_code}")
                if response.status_code == 200:
                    num_sent += 1
                    print(f"Successfully sent email to {message.to}")
                else:
                    print(f"Mailgun Error: {response.status_code} - {response.text}")
                    if not self.fail_silently:
                        pass 
            except Exception as e:
                print(f"Mailgun Exception: {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                if not self.fail_silently:
                    pass 
        return num_sent
