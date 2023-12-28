from django.db import models
from users.models import CustomUser,Employee
from project.models import Projects
from django.utils import timezone
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import json
import channels.layers
from asgiref.sync import async_to_sync
from notifications.signals import notify
from notification.models import Notification
from notification.serializers import NotificationSerializer
STATUS = (
    ("incomplete", "Incomplete"),
    ("todo", "To Do"),
    ("doing", "Doing"),
    ("completed", "Completed"),
)

PRIORITY = (
    ("medium", "Medium"),
    ("high", "High"),
    ("low", "Low"),
)
class Task(models.Model):
    project = models.ForeignKey(Projects,on_delete=models.CASCADE,related_name="project")
    # assigned_to = models.ForeignKey(CustomUser,null=True, blank=True,on_delete=models.SET_NULL,related_name="tasks")
    assigned_to = models.ManyToManyField(Employee)
    title = models.CharField(max_length=100,default="Task Title")
    description = models.TextField(max_length=300,default=None,null=True,blank=True)
    start_date = models.DateField(default=None,null=True,blank=True)
    deadline = models.DateField(default=None,null=True,blank=True)
    task_finished = models.DateTimeField(default=None,null=True,blank=True)
    progress = models.IntegerField(default=0)
    added_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=1)
    status = models.CharField(choices=STATUS, max_length=10, default="notstarted")
    priority = models.CharField(choices=PRIORITY, max_length=10, default="low")
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    deleted_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Tasks"
        ordering = ['-id']

    def __str__(self):
        return self.title

# @receiver(post_save, sender=Task)
# def create_project_notification(sender, instance, created, **kwargs):
#     if created:
#         message = f"You have a new task: {instance.title} from {instance.added_by}"  # Customize as needed
#         notify.send(instance.added_by, recipient=instance.assigned_to, verb='You have a new task', target=instance)
        
#         user_to_notify = instance.assigned_to
#         print(user_to_notify.id)
#         last_notification = Notification.objects.order_by('-timestamp').first()
        

#         # Send notification to the user through WebSocket
#         channel_layer = channels.layers.get_channel_layer()
#         serializer = NotificationSerializer(last_notification)
#         serialized_notification = serializer.data
        
#         async_to_sync(channel_layer.group_send)(
#             f"notification_{user_to_notify.id}",
#             {
#                 'command':'task_status',
#                 'type': 'send_notification',
#                 'message': json.dumps(serialized_notification)
#             }
#         )
        
class File(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to='task_files/')
    file_name = models.TextField(max_length=100,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Files"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.task.title} - {self.file.name}"
    

# class TaskMembers(models.Model):
#     task = models.ForeignKey(Task,on_delete=models.CASCADE)
#     user = models.ForeignKey()


class BroadcastNotification(models.Model):
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']

@receiver(post_save,sender=BroadcastNotification)
def notification_handler(sender,instance,created,**kwargs):

    # user_to_notify = instance.assignee
    message = f"You have a new task: {instance.message}"  # Customize as needed

    # Send notification to the user through WebSocket
    channel_layer = channels.layers.get_channel_layer()
   
    
    async_to_sync(channel_layer.group_send)(
        "notification_all",
        {
            'type': 'send_notification',
            'message': json.dumps(message)
        }
    )

    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-"+str(instance.id), task="task.tasks.broadcast_notification", args=json.dumps((instance.id,)))

    #if not created:
