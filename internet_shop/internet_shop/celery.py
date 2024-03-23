import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "internet_shop.settings")

app = Celery("internet_shop")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "check_not_mailed_orders_task": {
        "task": "orders.tasks.check_not_mailed_orders_task",
        "schedule": crontab(minute="*/1"),
    },
}
