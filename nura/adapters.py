from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class NuraAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        key = emailconfirmation.key
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
        return f"{frontend_url}/auth/verify-email/{key}"

    def send_mail(self, template_prefix, email, context):
        context['frontend_url'] = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
        super().send_mail(template_prefix, email, context)
