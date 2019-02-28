from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..authentication import TokenAPIAuthentication
from ..models import Route
from ..serializers import RouteSerializer


class RouteViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    lookup_field = "pk"
    authentication_classes = (TokenAPIAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    throttle_classes = []

    def create(self, request):
        payload = request.data

        data = {"endpoint": payload.get("endpoint", None)}

        r = Route(**data)
        r.save()

        return Response(status=status.HTTP_200_OK)
