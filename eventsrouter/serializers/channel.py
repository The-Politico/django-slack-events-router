# flake8: noqa
from rest_framework import serializers
from eventsrouter.models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"
