from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import Group
from .models import Employee


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password','username']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'groups','first_name','last_name','profile_pic']
        extra_kwargs = {'profile_pic': {'required': False}}



class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']

class EmployeeSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)
    class Meta:
        model = Employee
        fields = '__all__'
    def update(self, instance, validated_data):
        # Check if 'profile_pic' is present in the validated_data
        profile_pic = validated_data.get('profile_pic')

        if profile_pic is not None:
            # Handle the case when a new file is provided
            instance.profile_pic = profile_pic
            # ... any additional logic related to updating the profile_pic field

        # Continue with the regular update logic
        return super().update(instance, validated_data)

class EmployeeListSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    user = CustomUserSerializer()
    class Meta:
        model= Employee
        fields = '__all__'



class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)


