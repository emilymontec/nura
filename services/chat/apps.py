from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate

def setup_site_domain(sender, **kwargs):
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    domain = frontend_url.replace('http://', '').replace('https://', '').split('/')[0]
    try:
        from django.contrib.sites.models import Site
        Site.objects.update_or_create(
            id=getattr(settings, 'SITE_ID', 1),
            defaults={'domain': domain, 'name': 'NURA'}
        )
    except Exception:
        pass

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        import chat.views
        post_migrate.connect(setup_site_domain, sender=self)
