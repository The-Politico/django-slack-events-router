# Generated by Django 2.1.7 on 2019-02-28 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventsrouter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.URLField(unique=True)),
                ('verified', models.BooleanField(default=False)),
                ('channel_filters', models.ManyToManyField(blank=True, related_name='channel_filters', to='eventsrouter.Channel')),
                ('event_filters', models.ManyToManyField(blank=True, related_name='event_filters', to='eventsrouter.Event')),
            ],
        ),
    ]