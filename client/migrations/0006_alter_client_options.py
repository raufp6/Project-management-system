# Generated by Django 4.2.1 on 2023-11-10 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_alter_client_deleted_at_alter_client_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Clients'},
        ),
    ]
