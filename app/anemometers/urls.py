from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AnemometerViewSet, SpeedStatsWithinRadiusView, WindReadingViewSet

router = DefaultRouter(trailing_slash=False)
router.register(prefix="anemometers", viewset=AnemometerViewSet, basename="anemometers")
router.register(prefix="readings", viewset=WindReadingViewSet, basename="readings")

urlpatterns = [
    path(
        "readings/radius/stats",
        SpeedStatsWithinRadiusView.as_view(),
        name="readings-radius-stats",
    ),
] + router.urls
