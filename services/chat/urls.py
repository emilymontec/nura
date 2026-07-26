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
    path('profile/', views.user_profile, name='user_profile'),
    path('profile', views.user_profile, name='user_profile-no-slash'),
    path('workspace/', views.user_workspace, name='user_workspace'),
    path('workspace', views.user_workspace, name='user_workspace-no-slash'),

    # Dataset endpoints
    path('datasets/', views.dataset_list_create, name='dataset_list_create'),
    path('datasets', views.dataset_list_create, name='dataset_list_create-no-slash'),
    path('datasets/<int:pk>/', views.dataset_detail, name='dataset_detail'),
    path('datasets/<int:pk>', views.dataset_detail, name='dataset_detail-no-slash'),
    path('datasets/<int:pk>/activate/', views.dataset_activate, name='dataset_activate'),
    path('datasets/<int:pk>/activate', views.dataset_activate, name='dataset_activate-no-slash'),

    # File management endpoints
    path('datasets/<int:pk>/rename/', views.dataset_rename, name='dataset_rename'),
    path('datasets/<int:pk>/rename', views.dataset_rename, name='dataset_rename-no-slash'),
    path('datasets/<int:pk>/move/', views.dataset_move, name='dataset_move'),
    path('datasets/<int:pk>/move', views.dataset_move, name='dataset_move-no-slash'),
    path('datasets/<int:pk>/star/', views.dataset_toggle_star, name='dataset_toggle_star'),
    path('datasets/<int:pk>/star', views.dataset_toggle_star, name='dataset_toggle_star-no-slash'),
    path('datasets/bulk-delete/', views.dataset_bulk_delete, name='dataset_bulk_delete'),
    path('datasets/bulk-delete', views.dataset_bulk_delete, name='dataset_bulk_delete-no-slash'),
    path('datasets/stats/', views.dataset_stats, name='dataset_stats'),
    path('datasets/stats', views.dataset_stats, name='dataset_stats-no-slash'),

    # Category endpoints
    path('categories/', views.category_list_create, name='category_list_create'),
    path('categories', views.category_list_create, name='category_list_create-no-slash'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>', views.category_detail, name='category_detail-no-slash'),
]
