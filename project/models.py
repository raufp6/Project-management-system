from django.db import models
from django.utils import timezone
from datetime import date
from client.models import Client
from users.models import CustomUser


STATUS = (
    ("inprogress", "In Progress"),
    ("notstarted", "Not started"),
    ("onhold", "On Hold"),
    ("canceled", "Canceled"),
    ("finished", "Finished"),
)

PRIORITY = (
    ("hot", "Hot"),
    ("warm", "Warm"),
    ("low", "Low"),
)
# Create your models here.
class Projects(models.Model):
    name = models.CharField(max_length=100,default="Project Title")
    description = models.TextField(max_length=300,default=None,null=True,blank=True)
    start_date = models.DateField(default=None,null=True,blank=True)
    deadline = models.DateField(default=None,null=True,blank=True)
    # project_created = models.DateTimeField(default=None,null=True,blank=True)
    project_finished = models.DateTimeField(default=None,null=True,blank=True)
    progress = models.IntegerField(default=0)
    client = models.ForeignKey(Client,on_delete=models.CASCADE, null=True)
    added_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=1)
    status = models.CharField(choices=STATUS, max_length=10, default="notstarted")
    priority = models.CharField(choices=PRIORITY, max_length=10, default="low")
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    deleted_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Projects"
        ordering = ['-id']

    def __str__(self):
        return self.name


