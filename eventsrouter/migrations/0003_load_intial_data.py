from django.db import migrations, IntegrityError, transaction
import os
from django.core import serializers


fixture_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../fixtures")
)
fixture_filename = "initial_data.json"


def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_dir, fixture_filename)

    fixture = open(fixture_file, "rb")
    objects = serializers.deserialize("json", fixture, ignorenonexistent=True)
    for obj in objects:
        try:
            with transaction.atomic():
                obj.save()
        except IntegrityError:
            pass
    fixture.close()


def unload_fixture(apps, schema_editor):
    "Brutally deleting all entries for this model..."

    Event = apps.get_model("eventsrouter", "Event")
    Event.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("eventsrouter", "0001_initial"),
        ("eventsrouter", "0002_event_route"),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture)
    ]
