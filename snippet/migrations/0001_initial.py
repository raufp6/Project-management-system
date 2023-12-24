# Generated by Django 4.2.6 on 2023-11-01 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('code', models.TextField()),
                ('linenos', models.BooleanField(default=False)),
                ('language', models.CharField(choices=[('ml', 'Malayalam'), ('en', 'Englis')], default='python', max_length=100)),
                ('style', models.CharField(choices=[('top', 'Top'), ('bottom', 'Bottom')], default='friendly', max_length=100)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
