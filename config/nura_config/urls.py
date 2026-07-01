from django.contrib import admin
from django.urls import include, path
# We need to add services/ to sys.path to import chat
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'services'))
from chat import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chat.urls')),
    path('', views.index, name='home'),
    path('chat/', views.chat, name='chat'),
]
