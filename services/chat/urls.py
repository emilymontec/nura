from django.urls import path, re_path
from . import views


urlpatterns = [
    path('test/', views.test_endpoint, name='test'),
    path('test', views.test_endpoint, name='test-no-slash'),
    path('analyze/', views.analyze_endpoint, name='analyze'),
    path('analyze', views.analyze_endpoint, name='analyze-no-slash'),
    path('chat/', views.chat_endpoint, name='chat'),
    path('chat', views.chat_endpoint, name='chat-no-slash'),
    path('sessions/', views.list_sessions, name='list_sessions'),
    path('sessions', views.list_sessions, name='list_sessions-no-slash'),
    path('sessions/<str:session_id>/', views.get_session_history, name='get_session_history'),
    path('sessions/<str:session_id>', views.get_session_history, name='get_session_history-no-slash'),
    path('sessions/<str:session_id>/rename/', views.rename_session, name='rename_session'),
    path('sessions/<str:session_id>/rename', views.rename_session, name='rename_session-no-slash'),
    path('sessions/<str:session_id>/delete/', views.delete_session, name='delete_session'),
    path('sessions/<str:session_id>/delete', views.delete_session, name='delete_session-no-slash'),
]
