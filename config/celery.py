import os
from celery import Celery
from celery.schedules import crontab
#from celery.task.schedules import Schedule

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object(f'django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'send-daily-reminders': {
#         'task': 'tasks.schedule_reminders',
#         'schedule': crontab(hour=0, minute=0),  # Выполнять ежедневно в 00:00
#     },
# }

# Запуск Celery Beat
app.start()
