from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('start-backup/', views.start_backup, name='start_backup'),
    path('backup-progress/<str:task_id>/', views.backup_progress, name='backup_progress'),
    path('backup-page/', views.backup_page, name='backup_page'),
    path('start-backup-ajax/', views.start_backup_ajax, name='start_backup_ajax'),
    path('restore-page/', views.restore_page, name='restore_page'),
    path('start-restore-ajax/', views.start_restore_ajax, name='start_restore_ajax'),
    path('update-page/', views.update_page, name='update_page'),
    path('start-update-ajax/', views.start_update_ajax, name='start_update_ajax'),
] 