"""
Use this file to configure pluggable app settings and resolve defaults
with any overrides set in project settings.
"""

from django.conf import settings as project_settings


class Settings:
    pass


Settings.SLACK_VERIFICATION_TOKEN = getattr(
    project_settings, "EVENTSROUTER_SLACK_VERIFICATION_TOKEN", ""
)

Settings.AUTH_DECORATOR = getattr(
    project_settings,
    "EVENTSROUTER_AUTH_DECORATOR",
    "django.contrib.auth.decorators.staff_member_required",
)

Settings.SECRET_KEY = getattr(
    project_settings, "EVENTSROUTER_SECRET_KEY", "a-bad-secret-key"
)

settings = Settings
