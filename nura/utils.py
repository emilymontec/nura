from django.conf import settings

def custom_password_reset_url_generator(request, user, temp_key):
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
    return f"{frontend_url}/reset-password/{user.pk}/{temp_key}/"
