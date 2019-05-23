from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from toolbox.django.rest.authentication.slack import SlackSignedAuthentication
from ..models import Route
from ..celery import post_webhook


class Events(APIView):
    authentication_classes = (SlackSignedAuthentication,)
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        slack_message = request.data

        # Handle Slack's URL verification challenge
        # https://api.slack.com/events/url_verification
        if slack_message.get("type") == "url_verification":
            return Response(
                data=slack_message.get("challenge"), status=status.HTTP_200_OK
            )

        if "event" in slack_message:
            channel_id = get_channel_id(slack_message)

            event_name = slack_message.get("event", {}).get("type", "")

            routes = Route.objects.all()

            # We forward Slack's verification headers so downstream apps can
            # choose to also verify requests.
            headers = {
                "X-SLACK-REQUEST-TIMESTAMP": request.META.get(
                    "HTTP_X_SLACK_REQUEST_TIMESTAMP"
                ),
                "X-SLACK-SIGNATURE": request.META.get(
                    "HTTP_X_SLACK_SIGNATURE"
                ),
            }

            for route in routes:
                if filter_route_by_channel(
                    route, channel_id
                ) and filter_route_by_event(route, event_name):
                    post_webhook.delay(
                        endpoint=route.endpoint,
                        data=slack_message,
                        headers=headers,
                    )

        return Response(status=status.HTTP_200_OK)


def get_channel_id(data):
    """Gets channel id in a few of the different ways Slack sends it."""
    channel_id = data.get("event", {}).get("channel", None)
    if channel_id is None:
        channel_id = data.get("event", {}).get("item", {}).get("channel", None)
    if channel_id is None:
        channel_id = data.get("event", {}).get("channel_id", None)

    return channel_id


def filter_route_by_channel(route, api_id):
    if not api_id:
        return True

    filters = route.channel_filters
    if filters.count() == 0:
        return True

    return filters.filter(api_id=api_id).count() > 0


def filter_route_by_event(route, name):
    filters = route.event_filters
    if filters.count() == 0:
        return True

    return filters.filter(name=name).count() > 0
