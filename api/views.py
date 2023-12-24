from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import viewsets


from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.views import APIView
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser
from .serializers import CombinedSerializer
from .serializers import UserSerializer,ClientSerializer,ProjectsSerializer,MyTokenObtainPairSerializer
from client.models import Client
from users.models import CustomUser
from project.models import Projects
from django.contrib.auth.models import Group
import datetime
from rest_framework import permissions,authentication
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["GET"])
def api_home(request,*args, **kwargs):
    return Response({"message":"Hello world"})




    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserView(APIView):
    
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

class CreateUserView(APIView):

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account=serializer.save()
            data['response'] = 'registered'
            data['username'] = account.username
            data['email'] = account.email
        else:
            data=serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)
    
# class CreateClientView(APIView):
#     def post(self, request, format=None):
#         serializer = ClientSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             # account=serializer.save()
#             data['response'] = 'registered'
#             # data['username'] = account.username
#             # data['email'] = account.email
#         else:
#             data=serializer.errors
#             return Response(data)

#         # def perform_create(self, serializer):
#         #     user = CustomUser.objects.get(email=serializer.email)
#         #     serializer.user = user
#         #     serializer.save()
#     def perform_create(self, serializer):
#         user = CustomUser.objects.get(email=serializer.validated_data.get('email'))
            
#         serializer.save(user=user)
        
#     data['response'] = 'registered'
        
#     return Response(data)

class CreateClientView(APIView):
    def post(self, request, format=None):
        # Check your conditions here (e.g., check if a client with a specific condition exists)
        # if not Client.objects.filter(your_condition).exists():
        #     return Response({'error': 'Client condition not met.'}, status=status.HTTP_400_BAD_REQUEST)

        # If the conditions are met, proceed with user creation
        serializer = ClientSerializer(data=request.data['client'])
        if serializer.is_valid():
            # CUstomsSer = UserSerializer(data=request.data['contact'])
            # if serializer.is_valid():
            #     pass
            user = CustomUser.objects.get(email=serializer.validated_data['email'])
            client = Client.objects.create(
                company_name=serializer.validated_data['company_name'],
                user=user,
                phone=serializer.validated_data['phone'],
                website=serializer.validated_data['website'],
                
            )
            data = {}
            data['response'] = 'registered'
            return Response(data, status=status.HTTP_201_CREATED)
        
        data = serializer.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

class CreateUserAndClientView(APIView):
    def post(self, request, format=None):
        serializer = CombinedSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data['user']
            client_data = serializer.validated_data['client']

            # Create the User
            user = CustomUser.objects.create(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )

            # Create the Client associated with the User
            client = Client(user=user, **client_data)
            client.save()
            data =[]
            data['response'] = 'done'
            

            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ClientListView(ListCreateAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     # filter_backends = [SearchFilter]
#     # search_fields = ['email', 'username']

class ClientListView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    def get(self, request, format=None):
        # You can customize the filtering logic based on your requirements
        clients = Client.objects.all()  # Retrieve all clients

        # Serialize the list of clients
        serializer = ClientSerializer(clients, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account=serializer.save()
        else:
            data=serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)
    


# class ClientDetails(RetrieveUpdateDestroyAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     lookup_field = 'id'



class ClientDetails(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        user_data = serializer.validated_data.get('user', {})

        # Exclude username and password from user_data
        user_data.pop('username', None)
        user_data.pop('password', None)
        user_data.pop('email', None)

        serializer.save()


class ProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # You can customize the filtering logic based on your requirements
        clients = Projects.objects.all()  # Retrieve all clients

        # Serialize the list of clients
        serializer = ProjectsSerializer(clients, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
