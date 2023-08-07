import os
from celery.schedules import crontab
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_crm.settings')

app = Celery('admin_crm')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.update(
    timezone='UTC',
    enable_utc=True,
)


app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-morning': {
        'task': 'tasks.approval',
        'schedule': crontab(minute=0, hour='*/2'),
        'args': (16, 16),
    },
}