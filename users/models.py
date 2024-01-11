from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
import uuid
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    is_client = models.BooleanField(default=False)
    is_emp = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to="uploads/user/",default="uploads/user.png")
    # group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    updated_at = models.DateTimeField(null=True,blank=True,auto_now=True)
    deleted_at = models.DateTimeField(null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    
    
    class Meta:
        verbose_name_plural = "Users"
        ordering = ['-id']

    def __str__(self):
        return self.email



def generate_emp_id():
    return uuid.uuid4().hex[:10].upper()

class Employee(models.Model):
    emp_id = models.CharField(default=generate_emp_id, max_length=50, editable=False)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, default=None,null=True,blank=True)
    # profile_pic = models.ImageField(upload_to="uploads/emp/",default="uploads/user.png")
    joined_date = models.DateField(null=True,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True,auto_now_add=True)
    updated_at = models.DateField(null=True,blank=True,auto_now=True)
    deleted_at = models.DateField(null=True,blank=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name_plural = "Employees"
        ordering = ['-created_at']

    def __str__(self):
        return self.user.first_name +" "+self.user.last_name
    

class OnlineUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name




        
        
        
        