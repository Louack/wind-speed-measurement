from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from .filters import AnemometerFilterSet
from .models import Anemometer
from .serializers.model_serializers import AnemometerSerializer


class AnemometerViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = AnemometerSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Anemometer.objects.all().order_by("name")
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AnemometerFilterSet
    ordering_fields = ["id", "name"]
