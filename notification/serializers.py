from rest_framework import serializers
from notifications.models import Notification
from users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    recipient_data = UserSerializer(source='recipient', read_only=True)
    actor_data = UserSerializer(source='actor', read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'
