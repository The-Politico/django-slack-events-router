from django.urls import include, path
from rest_framework import routers

from .views import Events
from .viewsets import ChannelViewset, RouteViewset

router = routers.DefaultRouter()
router.register(r"channel", ChannelViewset, base_name="slack-events-channel")
router.register(r"route", RouteViewset, base_name="slack-events-route")

urlpatterns = [
    path("api/", include(router.urls)),
    path("events/", Events.as_view()),
]
