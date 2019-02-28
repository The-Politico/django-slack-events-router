from django.db import models


class Event(models.Model):
    """
    An event that can be filtered for.
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
