from django.db import models
from django.utils import timezone
from datetime import date
from users.models import CustomUser

STATUS = (
    ("blocked", "Blocked"),
    ("active", "active")
)
class Client(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
    company_name = models.CharField(max_length=100,default='Company name')    
    email = models.CharField(max_length=100,default=None,blank=True,null=True)    
    phone = models.CharField(max_length=20, default=None,null=True,blank=True)
    contact_person = models.CharField(max_length=100,blank=True,null=True)
    website = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(choices=STATUS, max_length=10, default="active")
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    updated_at = models.DateField(null=True,blank=True,auto_now=True)
    deleted_at = models.DateField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Clients"
        ordering = ['-id']

    def __str__(self):
        return self.company_name

