from rest_framework import serializers
from .models import ChatRoom, ChatMessage
from users.serializers import CustomUserSerializer

class ChatRoomSerializer(serializers.ModelSerializer):
	member = CustomUserSerializer(many=True, read_only=True)
	members = serializers.ListField(write_only=True)

	def create(self, validatedData):
		memberObject = validatedData.pop('members')
		chatRoom = ChatRoom.objects.create(**validatedData)
		chatRoom.member.set(memberObject)
		return chatRoom

	class Meta:
		model = ChatRoom
		exclude = ['id']

class ChatMessageSerializer(serializers.ModelSerializer):
	userName = serializers.SerializerMethodField()
	userImage = serializers.ImageField(source='user.profile_pic')

	class Meta:
		model = ChatMessage
		exclude = ['id', 'chat']

	def get_userName(self, Obj):
		return Obj.user.first_name + ' ' + Obj.user.last_name
