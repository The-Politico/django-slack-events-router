"""
Use this file to configure pluggable app settings and resolve defaults
with any overrides set in project settings.
"""

from django.conf import settings as project_settings


class Settings:
    pass


Settings.VERIFICATION_TOKEN = getattr(
    project_settings, "EVENTSROUTER_VERIFICATION_TOKEN", ""
)

settings = Settings
