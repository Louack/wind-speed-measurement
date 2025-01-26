from rest_framework.routers import DefaultRouter

from .views import AnemometerViewSet

router = DefaultRouter(trailing_slash=False)
router.register(prefix="anemometers", viewset=AnemometerViewSet, basename="anemometers")

urlpatterns = router.urls
