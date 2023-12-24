from rest_framework import serializers
from users.models import CustomUser
from task.models import Task
from project.serializers import ProjectSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskListSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer()  
    project = ProjectSerializer() 

    class Meta:
        model = Task
        fields = '__all__'






