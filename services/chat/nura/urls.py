from django.contrib import admin
from django.urls import include, path
from chat import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),
    path('', views.index, name='home'),
]
