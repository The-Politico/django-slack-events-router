import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings


class Test(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        slack_message = request.data

        if (
            slack_message.get("token")
            != settings.EVENTSROUTER_SLACK_VERIFICATION_TOKEN
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        if slack_message.get("type") == "url_verification":
            return Response(
                data=slack_message.get("challenge"), status=status.HTTP_200_OK
            )

        print("TEST WEBHOOK:")
        print(json.dumps(slack_message, indent=2))

        return Response(status=status.HTTP_200_OK)
