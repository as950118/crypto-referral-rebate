import os
from celery import Celery

# Django 설정을 Celery에 알려줍니다
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_rebate.settings')

app = Celery('crypto_rebate')

# Django 설정에서 Celery 설정을 가져옵니다
app.config_from_object('django.conf:settings', namespace='CELERY')

# 각 앱의 tasks.py 파일에서 작업을 자동으로 발견합니다
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 