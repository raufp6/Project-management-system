from django.contrib import admin
from .models import Task,BroadcastNotification

# Register your models here.
admin.site.register(Task)
admin.site.register(BroadcastNotification)