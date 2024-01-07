from django.db import models
from users.models import CustomUser
from shortuuidfield import ShortUUIDField

# class Message(models.Model):
#     sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
#     receiver = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.sender.first_name} to {self.receiver.first_name}: {self.content}'
    
class ChatRoom(models.Model):
	roomId = ShortUUIDField()
	type = models.CharField(max_length=10, default='DM')
	member = models.ManyToManyField(CustomUser)
	name = models.CharField(max_length=20, null=True, blank=True)

	def __str__(self):
		return self.roomId + ' -> ' + str(self.name)

class ChatMessage(models.Model):
	chat = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)
	user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
	message = models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.message
