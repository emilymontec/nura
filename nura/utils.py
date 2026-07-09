from django.conf import settings

def custom_password_reset_url_generator(request, user, temp_key):
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
    return f"{frontend_url}/auth/password-reset/confirm/{user.pk}/{temp_key}"
