import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from toolbox.django.rest.authentication.slack import SlackSignedAuthentication


class Test(APIView):
    authentication_classes = (SlackSignedAuthentication,)
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        slack_message = request.data

        if slack_message.get("type") == "url_verification":
            return Response(
                data=slack_message.get("challenge"), status=status.HTTP_200_OK
            )

        print("TEST WEBHOOK:")
        print(json.dumps(slack_message, indent=2))

        return Response(status=status.HTTP_200_OK)
