from rest_framework import viewsets,authentication,filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer,GroupSerializer,UserRegistrationSerializer,EmployeeSerializer
from .models import CustomUser,Employee
from django.contrib.auth.models import Group
import datetime
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsStaffPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied


class GroupViewSet(ListCreateAPIView):
    permission_classes = [IsStaffPermission]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = '__all__' 
    search_fields = ['^username','^email']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserRegViewSet(ListCreateAPIView):
    
    # queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = '__all__' 
    search_fields = ['^username','^email']
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsStaffPermission]

    def get_queryset(self):
        print("get user ...")
        if self.request.method == 'GET' and self.request.GET and self.request.GET['usertype'] =='emp':
            return CustomUser.objects.filter(is_emp=True,deleted_at__isnull=True)    
        return CustomUser.objects.filter(is_staff=True,deleted_at__isnull=True)

    def perform_create(self, serializer):
        print("create user ...")
        user = serializer.save()
        user.is_staff = True  # Set is_staff to True
        user.is_emp = True
        # user.groups = list(self.request.data.get('group'))
        user.save()

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = CustomUser.objects.all()
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # Instead of deleting, update the deleted_at field
        instance.deleted_at = datetime.datetime.now().date()  # Make sure to import timezone
        instance.save()

class EmployeeViewSet(ListCreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsStaffPermission]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['first_name','last_name','status']
    # search_fields = ['^first_name','^last_name']
    # exclude = ('profile_pic')

    def perform_create(self, serializer):

        if not self.request.user.is_emp:

            raise PermissionDenied('Only staff members can add employees.')

        serializer.save()



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_count(request):
    user = request.user
    count = CustomUser.objects.count()
    
    return Response({'count':count})