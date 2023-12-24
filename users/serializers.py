from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.models import Group

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
        fields = ['id', 'username', 'password', 'email', 'groups']

# class UserRegistrationSerializer(serializers.ModelSerializer):

#     groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())


#     class Meta:

#         model = CustomUser

#         fields = ['id', 'username', 'password', 'email','groups']


#     def create(self, validated_data):

#         groups = validated_data.pop('groups')

#         user = CustomUser.objects.create(**validated_data)

#         user.groups.set(groups)

#         user.save()

#         return user