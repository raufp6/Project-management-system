from rest_framework import viewsets,authentication,filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer,GroupSerializer,UserRegistrationSerializer,EmployeeSerializer,UserCreationSerializer,CustomUserSerializer,EmployeeListSerializer
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
    # serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsStaffPermission]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['first_name','last_name','status']


    def get_serializer_class(self):
        return EmployeeListSerializer if self.request.method == 'GET' else EmployeeSerializer
    
    def create(self, request, *args, **kwargs):
       
        
        # Extract user-related data from the request
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'email': request.data.get('email'),
            'is_staff':True,
            'is_emp':True,
            'groups':request.data.getlist('groups')
        }
        employee_data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'phone': request.data.get('phone'),
            'profile_pic': request.data.get('profile_pic'),
            'joined_date': request.data.get('joined_date'),
            
        }
        
        # Create a user using the UserCreationSerializer
        group_ids = request.data.getlist('groups')
        print(group_ids)
        # groups = Group.objects.filter(pk__in=group_ids)

        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.set_password(user_data['password'])
        # user.groups.set(groups)  # Set the groups for the user
        user.save()


        # Add the user to the client data and create the client
        # client_data = request.data
        employee_data['user'] = user.id

        serializer = self.get_serializer(data=employee_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
class EmployeeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    # serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    permission_classes = [IsStaffPermission]
    lookup_field = 'pk'

    def get_serializer_class(self):
        return EmployeeListSerializer if self.request.method == 'GET' else EmployeeSerializer
    
    def perform_update(self, serializer):
        # Update Employee fields
        employee_instance = serializer.instance

        # Update CustomUser fields
        
        profile_pic = self.request.data.get('profile_pic', None)
        if profile_pic:
            print("None")
            employee_instance.profile_pic = profile_pic
        serializer.save()

        user_instance = employee_instance.user
        user_data = {
            'username': self.request.data.get('username'),
            # 'password': self.request.data.get('password'),
            'email': self.request.data.get('email'),
            
            'groups':self.request.data.getlist('groups')
        }
        print(self.request.data.getlist('groups'))
        user_serializer = CustomUserSerializer(user_instance, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

    def perform_destroy(self, instance):
        # Instead of deleting, update the deleted_at field
        instance.deleted_at = datetime.datetime.now().date()  # Make sure to import timezone
        instance.save()




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_count(request):
    user = request.user
    count = CustomUser.objects.count()
    
    return Response({'count':count})