from rest_framework import viewsets,filters
from rest_framework.response import Response
from .models import Client
from .models import CustomUser
from .serializers import ClientSerializer
from users.serializers import UserCreationSerializer
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView,UpdateAPIView
import datetime
from rest_framework import permissions,authentication
from django_filters.rest_framework import DjangoFilterBackend



class CreateClientView(ListCreateAPIView):
    # queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = '__all__' 
    search_fields = ['^company_name']
    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.DjangoModelPermissions]

    def get_queryset(self):
        return Client.objects.filter(deleted_at__isnull=True)

    def create(self, request, *args, **kwargs):
       
        
        # Extract user-related data from the request
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'email': request.data.get('email'),
            'first_name':request.data.get('username'),
            'last_name':request.data.get('username'),
            'is_client':True
        }
        client_data = {
            'company_name': request.data.get('company_name'),
            'email': request.data.get('email'),
            'phone': request.data.get('phone'),
            'contact_person': request.data.get('contact_person'),
            'website': request.data.get('website'),
            
            
        }

        # Create a user using the UserCreationSerializer
        user_serializer = UserCreationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.set_password(user_data['password'])
        user.save()


        # Add the user to the client data and create the client
        # client_data = request.data
        client_data['user'] = user.id

        serializer = self.get_serializer(data=client_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
    def list(self, request, *args, **kwargs):
        # Override list method if needed
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ClientRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # Instead of deleting, update the deleted_at field
        instance.deleted_at = datetime.datetime.now().date()  # Make sure to import timezone
        instance.save()

    # def perform_update(self, serializer):
    #     user_data = serializer.validated_data.get('user', {})

    #     # Exclude username and password from user_data
    #     # user_data.pop('username', None)
    #     # user_data.pop('password', None)

        # serializer.save()
    # def perform_update(self, serializer):
    #     instance = serializer.save()
    #     instance.updated_at = datetime.datetime.now().date()
    

