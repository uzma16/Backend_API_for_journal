import os
from celery import Celery
from mindfulness import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindfulness.settings')

app = Celery('mindfulness')

# Read Celery configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'after-every-1-min': {
        'task': 'reminder_cron_job',
        'schedule': crontab(minute='*/1')
    },
    'everyday-at-12': {
        'task': 'last_login',
        'schedule': crontab(hour=12, minute=0)
    },
    'at-9am-and-9pm': {
        'task': 'prompt_cron_job',
        'schedule': crontab(minute='*/30'),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
