from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationView

schema_view = get_schema_view(
    openapi.Info(
        title="WindForLife",
        default_version="v1",
    ),
    public=True,
    permission_classes=[
        AllowAny,
    ],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/register", RegistrationView.as_view(), name="register"),
    path("auth/tokens", TokenObtainPairView.as_view(), name="get-tokens"),
    path("auth/tokens/refresh", TokenRefreshView.as_view(), name="refresh-tokens"),
    path("", include("anemometers.urls")),
    path("docs", schema_view.with_ui("swagger", cache_timeout=0), name="docs"),
]
