from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Route
from .celery import verify_webhook


@receiver(post_save, sender=Route)
def save_webhook(sender, instance, **kwargs):
    verify_webhook.delay(instance.pk)
