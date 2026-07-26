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

    # New dataset management endpoints
    path('datasets/<int:pk>/duplicate/', views.dataset_duplicate, name='dataset_duplicate'),
    path('datasets/<int:pk>/duplicate', views.dataset_duplicate, name='dataset_duplicate-no-slash'),
    path('datasets/<int:pk>/archive/', views.dataset_archive, name='dataset_archive'),
    path('datasets/<int:pk>/archive', views.dataset_archive, name='dataset_archive-no-slash'),
    path('datasets/<int:pk>/reanalyze/', views.dataset_reanalyze, name='dataset_reanalyze'),
    path('datasets/<int:pk>/reanalyze', views.dataset_reanalyze, name='dataset_reanalyze-no-slash'),
    path('datasets/<int:pk>/download/', views.dataset_download, name='dataset_download'),
    path('datasets/<int:pk>/download', views.dataset_download, name='dataset_download-no-slash'),
    path('datasets/merge/', views.dataset_merge, name='dataset_merge'),
    path('datasets/merge', views.dataset_merge, name='dataset_merge-no-slash'),

    # Versioning endpoints
    path('datasets/<int:pk>/versions/', views.dataset_versions, name='dataset_versions'),
    path('datasets/<int:pk>/versions', views.dataset_versions, name='dataset_versions-no-slash'),
    path('datasets/<int:pk>/versions/<int:version_pk>/restore/', views.dataset_restore_version, name='dataset_restore_version'),
    path('datasets/<int:pk>/versions/<int:version_pk>/restore', views.dataset_restore_version, name='dataset_restore_version-no-slash'),

    # Exploration endpoints
    path('datasets/<int:pk>/explore/', views.dataset_explore, name='dataset_explore'),
    path('datasets/<int:pk>/explore', views.dataset_explore, name='dataset_explore-no-slash'),
    path('datasets/<int:pk>/preview/', views.dataset_preview, name='dataset_preview'),
    path('datasets/<int:pk>/preview', views.dataset_preview, name='dataset_preview-no-slash'),
    path('datasets/<int:pk>/columns/', views.dataset_columns, name='dataset_columns'),
    path('datasets/<int:pk>/columns', views.dataset_columns, name='dataset_columns-no-slash'),
    path('datasets/<int:pk>/statistics/', views.dataset_statistics, name='dataset_statistics'),
    path('datasets/<int:pk>/statistics', views.dataset_statistics, name='dataset_statistics-no-slash'),
    path('datasets/<int:pk>/search/', views.dataset_search, name='dataset_search'),
    path('datasets/<int:pk>/search', views.dataset_search, name='dataset_search-no-slash'),
    path('datasets/<int:pk>/filter/', views.dataset_filter, name='dataset_filter'),
    path('datasets/<int:pk>/filter', views.dataset_filter, name='dataset_filter-no-slash'),

    # Tag endpoints
    path('datasets/<int:pk>/tags/add/', views.dataset_add_tags, name='dataset_add_tags'),
    path('datasets/<int:pk>/tags/add', views.dataset_add_tags, name='dataset_add_tags-no-slash'),
    path('datasets/<int:pk>/tags/remove/', views.dataset_remove_tags, name='dataset_remove_tags'),
    path('datasets/<int:pk>/tags/remove', views.dataset_remove_tags, name='dataset_remove_tags-no-slash'),

    # Tag management
    path('tags/', views.tag_list_create, name='tag_list_create'),
    path('tags', views.tag_list_create, name='tag_list_create-no-slash'),
    path('tags/<int:pk>/', views.tag_detail, name='tag_detail'),
    path('tags/<int:pk>', views.tag_detail, name='tag_detail-no-slash'),

    # Category endpoints
    path('categories/', views.category_list_create, name='category_list_create'),
    path('categories', views.category_list_create, name='category_list_create-no-slash'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>', views.category_detail, name='category_detail-no-slash'),
]
