from django.db import models
from .Channel import Channel
from .Event import Event


class Route(models.Model):
    """
    An endpoint to send event payloads to
    """

    endpoint = models.URLField(unique=True)
    verified = models.BooleanField(default=False)

    channel_filters = models.ManyToManyField(
        Channel,
        blank=True,
        name="channel_filters",
        help_text="Choose the channels you want to filter for (or leave it "
        + "blank to not filter any).",
    )

    event_filters = models.ManyToManyField(
        Event,
        blank=True,
        name="event_filters",
        help_text="Choose the events you want to filter for (or leave it "
        + "blank to not filter any).",
    )

    def __str__(self):
        return self.endpoint
