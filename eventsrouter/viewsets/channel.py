from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..authentication import TokenAPIAuthentication
from ..models import Channel
from ..serializers import ChannelSerializer


class ChannelViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    lookup_field = "api_id"
    authentication_classes = (TokenAPIAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    throttle_classes = []

    def create(self, request):
        payload = request.data

        data = {"api_id": payload.get("api_id", None)}

        c = Channel(**data)
        c.save()

        return Response(status=status.HTTP_200_OK)
