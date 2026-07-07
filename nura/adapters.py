from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class NuraAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        key = emailconfirmation.key
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
        return f"{frontend_url}/verify-email/{key}/"
