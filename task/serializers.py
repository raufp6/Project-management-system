from rest_framework import serializers
from users.models import CustomUser,Employee
from task.models import Task,File
from project.serializers import ProjectSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'uploaded_at']

class TaskListSerializer(serializers.ModelSerializer):
    assigned_to = EmployeeSerializer(many=True)  
    # assigned_to = serializers.ManyRelatedField(queryset=Employee.objects.all())
    project = ProjectSerializer() 
    

    class Meta:
        model = Task
        fields = '__all__'






