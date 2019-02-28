# flake8: noqa
from rest_framework import serializers
from eventsrouter.models import Route


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"
