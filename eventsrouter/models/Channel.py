from django.db import models


class Channel(models.Model):
    """
    A Slack channel that can be filtered for.
    """

    api_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.api_id
