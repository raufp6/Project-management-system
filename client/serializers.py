from rest_framework import serializers
from .models import Client
from users.models import CustomUser
from users.serializers import UserCreationSerializer



class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = '__all__'

class ClientListSerializer(serializers.ModelSerializer):
    
    user = UserCreationSerializer()  # Include the UserSerializer

    class Meta:
        model = Client
        fields = ('company_name', 'phone', 'website','email','user','contact_person')
        # extra_kwargs = {'user': {'read_only': True}}




    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

