import requests
from celery import shared_task
from eventsrouter.conf import settings


@shared_task(acks_late=True)
def post_webhook(endpoint, data):
    headers = {"Authorization": "Token {}".format(settings.VERIFICATION_TOKEN)}
    try:
        requests.post(endpoint, json=data, headers=headers, timeout=1)
    except requests.exceptions.Timeout:
        pass
