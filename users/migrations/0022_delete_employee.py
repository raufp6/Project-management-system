# Generated by Django 4.2.6 on 2023-12-21 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_employee_emp_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
