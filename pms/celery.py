from __future__ import absolute_import,unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE','pms.settings')

app = Celery('pms')
app.conf.enable_utc = False

app.conf.update(timezone = 'Aisa/Kolkata')

app.config_from_object(settings,namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    
}

app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')