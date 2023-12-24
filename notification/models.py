from django.db import models
from notifications.base.models import AbstractNotification
from django.contrib.auth.models import Group


class Notification(AbstractNotification):
    group = models.ForeignKey(Group,on_delete=models.SET_NULL,null=True,blank=True)

    class Meta(AbstractNotification.Meta):
        abstract = False