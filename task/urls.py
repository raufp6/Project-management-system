from django.urls import path,include
from . import views

from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)

from .views import TaskView,TaskRetrieveUpdateDestroyAPIView,TaskFilesAPIView,upload_file,delete_file
urlpatterns = [
    path('test/',views.test),
    path('test_not/',views.test_notification),
    path('', TaskView.as_view(), name='tasks'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('create/', TaskView.as_view(), name='create-task'),
    path('<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
    path('files/<int:pk>/', TaskFilesAPIView.as_view(), name='task-files'),
    path('file/<int:task_id>/upload/', upload_file, name='file-upload'),
    path('file/<int:file_id>/delete/', delete_file, name='file-delete'),

    path('<int:pk>/update/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='update-task'),
    path('<int:pk>/delete/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='delete-task'),
    path('count/', views.task_count, name='task_count'),
    
]