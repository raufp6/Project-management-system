from rest_framework import viewsets,authentication,filters
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView,UpdateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer,GroupSerializer,UserRegistrationSerializer,EmployeeSerializer,UserCreationSerializer,CustomUserSerializer,EmployeeListSerializer,ChangePasswordSerializer
from .models import CustomUser,Employee
from project.models import Projects
from django.contrib.auth.models import Group
import datetime
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsStaffPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework import status


class GroupViewSet(ListCreateAPIView):
    permission_classes = [IsStaffPermission]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = '__all__' 
    search_fields = ['^username','^email']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserRegViewSet(ListCreateAPIView):
    
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['first_name','last_name','username','email']
    search_fields = ['^username','^email']
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsStaffPermission]


    # def get_queryset(self):
    #     excludeUsersArr = []
    #     try:
    #         excludeUsers = self.request.query_params.get('exclude')
    #         if excludeUsers:
    #             userIds = excludeUsers.split(',')
    #             for userId in userIds:
    #                 excludeUsersArr.append(int(userId))
    #     except:
    #         return []
    #     return super().get_queryset().exclude(id__in=excludeUsersArr)
    
    def get_queryset(self):
        print("get user ...")
        excludeUsersArr = []
        try:
            excludeUsers = self.request.query_params.get('exclude')
            if excludeUsers:
                userIds = excludeUsers.split(',')
                for userId in userIds:
                    excludeUsersArr.append(int(userId))
        except:
            pass

        usertype = self.request.query_params.get('usertype')
        excludeUsers = self.request.query_params.get('exclude')
        print(usertype)
        if usertype =='emp':
            return CustomUser.objects.filter(is_emp=True,deleted_at__isnull=True).exclude(id__in=excludeUsersArr)
        
        return CustomUser.objects.filter(is_staff=True,deleted_at__isnull=True).exclude(id__in=excludeUsersArr)
        

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
    filterset_fields = ['user__first_name','user__last_name','status']


    def get_serializer_class(self):
        return EmployeeListSerializer if self.request.method == 'GET' else EmployeeSerializer
    
    def get_queryset(self):
        print("get user ...")
        if 'project' in self.request.GET:
            project_id = self.request.GET['project']
            project = get_object_or_404(Projects, pk=project_id)
            return project.members.filter(deleted_at__isnull=True)    
        return Employee.objects.filter(deleted_at__isnull=True)
    
    def create(self, request, *args, **kwargs):
       
        
        # Extract user-related data from the request
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            # 'profile_pic': request.data.get('profile_pic'),
            'is_staff':True,
            'is_emp':True,
            'groups':request.data.getlist('groups')
        }
        employee_data = {
            # 'first_name': request.data.get('first_name'),
            # 'last_name': request.data.get('last_name'),
            'phone': request.data.get('phone'),
            # 'profile_pic': request.data.get('profile_pic'),
            'joined_date': request.data.get('joined_date'),
            
        }
        
        # Create a user using the UserCreationSerializer
        group_ids = request.data.getlist('groups')
        print(group_ids)
        # groups = Group.objects.filter(pk__in=group_ids)

        user_serializer = UserRegistrationSerializer(data=user_data)
        # user_serializer.is_valid(raise_exception=True)
        if user_serializer.is_valid():
            user = user_serializer.save()
            user.set_password(user_data['password'])
            # user.groups.set(groups)  # Set the groups for the user
            user.save()
            

            
            # employee_serializer.is_valid(raise_exception=True)
            employee_data['user'] = user.id
            employee_serializer = self.get_serializer(data=employee_data)
            if employee_serializer.is_valid():
                self.perform_create(employee_serializer)
                headers = self.get_success_headers(employee_serializer.data)
                return Response(employee_serializer.data, status=201, headers=headers)
            else:
                # Rollback user creation in case of employee validation failure
                user.delete()
                return Response({'error': employee_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
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
            'first_name':self.request.data.get('first_name'),
            'last_name':self.request.data.get('last_name'),
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
"""
PASSWORD REST FOR LOGGED USER
"""
class PasswordChangeView(UpdateAPIView):
    model = CustomUser
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.POST)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            new_password2 = serializer.validated_data['new_password2']
            print(new_password2)
            # print(request.data.get('new_password2'))


            # Check if the old password is correct
            if not request.user.check_password(old_password):
                return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

            # Change the user's password
            form = PasswordChangeForm(user=request.user, data={'old_password':old_password,'new_password1': new_password, 'new_password2': new_password2})
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important to maintain the user's session
                return Response({'message': 'Password successfully changed.'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid input data.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self, queryset=None):
            obj = self.request.user
            return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
