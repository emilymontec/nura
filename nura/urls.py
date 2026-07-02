from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from chat.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),
    re_path(r'^.*$', index, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
