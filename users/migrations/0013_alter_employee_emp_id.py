# Generated by Django 4.2.6 on 2023-12-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_employee_emp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='emp_id',
            field=models.CharField(default='7CB99', editable=False, max_length=50, primary_key=True, serialize=False),
        ),
    ]
