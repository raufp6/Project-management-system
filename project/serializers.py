from rest_framework import serializers
from .models import Client
from users.models import CustomUser
from project.models import Projects
from client.serializers import ClientSerializer


class ProjectSerializer(serializers.ModelSerializer):
    # client = ClientSerializer()
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    class Meta:
        model = Projects
        fields = '__all__'

class ProjectListSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    class Meta:
        model = Projects
        fields = '__all__'






