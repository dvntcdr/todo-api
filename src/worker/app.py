from celery import Celery
from celery.schedules import crontab

from src.core.config import settings

celery_app = Celery(
    'todo',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['src.worker.tasks']
)

celery_app.autodiscover_tasks(['src.worker'])

celery_app.conf.beat_schedule = {
    'send-due-date-reminders': {
        'task': 'src.worker.tasks.send_due_date_reminders',
        'schedule': crontab(hour=8, minute=0)
        # 'schedule': 30.0,
    },
    'delete-refresh-tokens' : {
        'task': 'src.worker.tasks.cleanup_refresh_tokens',
        'schedule': crontab(hour=12, minute=0),
        # 'schedule': 30.0,
    }
}
