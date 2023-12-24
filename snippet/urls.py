from django.urls import path,include
from . import views

from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)


urlpatterns = [
    path('',views.snippet_list),
    
]