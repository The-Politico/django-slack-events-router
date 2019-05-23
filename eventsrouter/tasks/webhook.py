import requests
from celery import shared_task


@shared_task(acks_late=True)
def post_webhook(endpoint, data, headers):
    try:
        requests.post(endpoint, json=data, headers=headers, timeout=5)
    except requests.exceptions.Timeout:
        pass
