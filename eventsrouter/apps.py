from django.apps import AppConfig


class EventsrouterConfig(AppConfig):
    name = 'eventsrouter'

    def ready(self):
        from eventsrouter import signals  # noqa
