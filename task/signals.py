from django.db.models.signals import post_save, pre_delete
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Task
from notification.models import Notification
from notification.serializers import NotificationSerializer
from asgiref.sync import async_to_sync
from notifications.signals import notify
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import channels.layers
import json


@receiver(m2m_changed, sender=Task.assigned_to.through)
def create_task_notification(sender, instance, action, **kwargs):
    if action == "post_add" or action == "post_remove":
        message = f"You have a new task: {instance.title} from {instance.added_by}"  # Customize as needed
        for employee in instance.assigned_to.all():
            user_id = employee.user.id if employee.user else None
            print("--in--")
            print(user_id,"user")
            notify.send(instance.added_by, recipient=employee.user, verb='You have a new task', target=instance)
            
            user_to_notify = user_id
            
            last_notification = Notification.objects.order_by('-timestamp').first()
            

            # Send notification to the user through WebSocket
            channel_layer = channels.layers.get_channel_layer()
            serializer = NotificationSerializer(last_notification)
            serialized_notification = serializer.data
            
            async_to_sync(channel_layer.group_send)(
                f"notification_{user_to_notify}",
                {
                    'command':'task_status',
                    'type': 'send_notification',
                    'message': json.dumps(serialized_notification)
                }
            )