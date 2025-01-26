from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/register", RegistrationView.as_view(), name="register"),
    path("auth/tokens", TokenObtainPairView.as_view(), name="get-tokens"),
    path("auth/tokens/refresh", TokenRefreshView.as_view(), name="refresh-tokens"),
    path("", include("anemometers.urls")),
]
