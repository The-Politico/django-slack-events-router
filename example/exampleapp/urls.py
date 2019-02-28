from django.contrib import admin
from django.urls import include, path
from .views import Test

urlpatterns = [
    path("admin/", admin.site.urls),
    path("test/", Test.as_view()),
    path("", include("eventsrouter.urls")),
]
