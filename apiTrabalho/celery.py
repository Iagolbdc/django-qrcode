from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apiTrabalho.settings")

app = Celery("apiTrabalho.celery")

app.conf.beat_schedule = {
    'verificar-horarios': {
        'task': 'alunos.tasks.verificar_horarios',
        'schedule': crontab(minute=5, hour=2),  
    },
}

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)