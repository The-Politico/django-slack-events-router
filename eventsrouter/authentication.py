from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication, exceptions
from eventsrouter.conf import settings as app_settings


class TokenAPIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Don't enforce if DEBUG
        if settings.DEBUG:
            return (AnonymousUser, None)
        try:
            # Per DRF token auth, token is prefixed by string
            # literal "Token" plus whitespace, e.g., "Token <AUTHTOKEN>"
            token = request.META.get("HTTP_AUTHORIZATION").split()[1]
        except Exception:
            raise exceptions.AuthenticationFailed(
                "No token or incorrect token format"
            )

        if token == app_settings.VERIFICATION_TOKEN:
            return (AnonymousUser, None)
        raise exceptions.AuthenticationFailed("Unauthorized")
