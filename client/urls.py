from django.urls import path,include
from . import views

from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)

from .views import CreateClientView,ClientRetrieveUpdateDestroyAPIView
urlpatterns = [
    
    path('', CreateClientView.as_view(), name='clients'),
    path('create/', CreateClientView.as_view(), name='create-client'),
    # path('<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),
    path('<int:pk>/', ClientRetrieveUpdateDestroyAPIView.as_view(), name='client-view'),
    path('<int:pk>/update/', ClientRetrieveUpdateDestroyAPIView.as_view(), name='client-view'),
    path('<int:pk>/delete/', ClientRetrieveUpdateDestroyAPIView.as_view(), name='client-delete'),
    

]