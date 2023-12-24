from django.urls import path,include
from . import views


from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)

from .views import ProjectView,ProjectRetrieveUpdateDestroyAPIView
urlpatterns = [
    path('', ProjectView.as_view(), name='projects'),
    path('create/', ProjectView.as_view(), name='create-project'),
    path('<int:pk>/', ProjectRetrieveUpdateDestroyAPIView.as_view(), name='project-detail'),
    path('<int:pk>/update/', ProjectRetrieveUpdateDestroyAPIView.as_view(), name='update-project'),
    path('<int:pk>/delete/', ProjectRetrieveUpdateDestroyAPIView.as_view(), name='delete-project'),
    path('count/', views.project_count, name='project_count'),
]