# Generated by Django 4.2.6 on 2023-10-30 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_client_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
