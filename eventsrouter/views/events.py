from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from eventsrouter.conf import settings
from ..models import Route
from ..celery import post_webhook


class Events(APIView):
    # Open API
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        slack_message = request.data

        # import json
        #
        # print("DEBUG eventsrouter log:")
        # print(json.dumps(slack_message, indent=2))

        if slack_message.get("token") != settings.SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if slack_message.get("type") == "url_verification":
            return Response(
                data=slack_message.get("challenge"), status=status.HTTP_200_OK
            )

        if "event" in slack_message:
            channel_id = get_channel_id(slack_message)

            event_name = slack_message.get("event", {}).get("type", "")

            routes = Route.objects.filter(verified=True)

            for route in routes:
                if filter_route_by_channel(
                    route, channel_id
                ) and filter_route_by_event(route, event_name):
                    post_webhook.delay(route.endpoint, slack_message)

        return Response(status=status.HTTP_200_OK)


def get_channel_id(data):
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
    if len(filters.all()) == 0:
        return True

    return len(filters.filter(api_id=api_id)) > 0


def filter_route_by_event(route, name):
    filters = route.event_filters
    if len(filters.all()) == 0:
        return True

    return len(filters.filter(name=name)) > 0
