from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Employee

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

    list_display = ('username', 'email', 'is_active','is_staff','is_client', 'is_superuser','is_emp', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser','is_emp')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password','first_name','last_name','profile_pic')}),
        ('Permissions', {'fields': ('is_client','is_staff', 'is_active',
         'is_superuser','is_emp','groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active','is_client','is_emp','first_name','last_name')}
         ),
    )
    search_fields = ('email',)
    ordering = ('-id',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Employee)