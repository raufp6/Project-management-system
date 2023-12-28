from rest_framework import serializers
from .models import Client
from users.models import CustomUser,Employee
from project.models import Projects
from client.serializers import ClientSerializer
from users.serializers import EmployeeSerializer


class ProjectSerializer(serializers.ModelSerializer):
    # client = ClientSerializer()
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    
    class Meta:
        model = Projects
        fields = '__all__'

class ProjectListSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    members = EmployeeSerializer(many=True)
    class Meta:
        model = Projects
        fields = '__all__'







