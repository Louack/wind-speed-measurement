from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import RegistrationView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/register", RegistrationView.as_view(), name="register"),
    path("auth/tokens", TokenObtainPairView.as_view(), name="get-tokens"),
    path("auth/tokens/refresh", TokenRefreshView.as_view(), name="refresh-tokens"),
]
