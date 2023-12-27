from django.urls import path,include
from . import views


from .views import GroupViewSet,UserRegViewSet,UserRetrieveUpdateDestroyAPIView,EmployeeViewSet

urlpatterns = [
    path('',UserRegViewSet.as_view(),name='user'),
    path('employee/',EmployeeViewSet.as_view(),name='employee'),
    path('group/',GroupViewSet.as_view(),name='user-group'),
    path('create/',UserRegViewSet.as_view(),name='create-user'),
    path('<int:pk>',UserRetrieveUpdateDestroyAPIView.as_view(),name="user-detail"),
    path('<int:pk>/update/',UserRetrieveUpdateDestroyAPIView.as_view(),name="user-detail"),
    path('<int:pk>/delete/',UserRetrieveUpdateDestroyAPIView.as_view(),name="user-detail"),
    path('count/', views.user_count, name='user_count'),

]

