from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError, ImageField
from users.models import CustomUser
from client.models import Client
from project.models import Projects

from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # groups = 
    class Meta:
        model = CustomUser
        fields = ('id','username', 'email', 'password','groups')
        extra_kwargs = {'password': {'write_only': True}}

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['is_client'] = user.is_client
        # token['group'] = user.group.name
        token['groups'] = list(user.groups.values_list('name', flat=True))


        return token





class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Include the UserSerializer
    class Meta:
        model = Client
        fields = ('company_name', 'phone', 'website','email','user','contact_person','id')

class CombinedSerializer(serializers.Serializer):
    user = UserSerializer()
    client = ClientSerializer()


class ProjectsSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    class Meta:
        model = Projects
        fields = ('name', 'start_date', 'deadline','client','status')










