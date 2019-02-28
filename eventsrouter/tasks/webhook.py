import requests
import uuid
import re
from celery import shared_task
from eventsrouter.conf import settings
from eventsrouter.models import Route


@shared_task(acks_late=True)
def post_webhook(endpoint, data):
    requests.post(endpoint, json=data)


@shared_task(acks_late=True)
def verify_webhook(pk):
    route = Route.objects.get(pk=pk)
    if not route.verified:
        challenge = uuid.uuid4().hex[:10]
        response = requests.post(
            route.endpoint,
            json={
                "token": settings.SLACK_VERIFICATION_TOKEN,
                "type": "url_verification",
                "challenge": challenge,
            },
        )
        if response.status_code == requests.codes.ok:
            if clean_response(response.text) == challenge:
                route.verified = True
                route.save()


def clean_response(response):
    """ Cleans string quoting in response. """
    response = re.sub("^['\"]", "", response)
    response = re.sub("['\"]$", "", response)
    return response
