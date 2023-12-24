from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)

from .views import MyTokenObtainPairView
from .views import CreateUserAndClientView,CreateUserView,CreateClientView,ClientListView,ClientDetails,ProjectListView,UserView,LogoutView
urlpatterns = [
    path('',views.api_home),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('userinfo/', UserView.as_view(), name='userinfo'),
    path('logout/', LogoutView.as_view(), name='logout'),

]