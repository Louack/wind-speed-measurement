from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Avg, Max, Min, QuerySet
from django.db.models.functions import Round
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import AnemometerFilterSet, WindReadingFilterSet
from .models import Anemometer, WindSpeedReadings
from .serializers.model_serializers import (
    AnemometerRetrieveSerializer,
    AnemometerSerializer,
    WindReadingSerializer,
)
from .serializers.query_serializers import SpeedStatsWithinRadiusQuerySerializer
from .serializers.response_serializers import SpeedStatsWithinRadiusResponseSerializer


class AnemometerViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = AnemometerSerializer
    queryset = Anemometer.objects.all().order_by("name")
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AnemometerFilterSet
    ordering_fields = ["id", "name"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AnemometerRetrieveSerializer
        return AnemometerSerializer

    @swagger_auto_schema(responses={200: WindReadingSerializer})
    @action(detail=True, methods=["get"], url_path="readings")
    def get_readings(self, request, pk=None):
        anemometer = self.get_object()
        readings = anemometer.wind_readings.all().order_by("-date")

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_readings = paginator.paginate_queryset(readings, request)

        serializer = WindReadingSerializer(paginated_readings, many=True)

        return paginator.get_paginated_response(serializer.data)


class WindReadingViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = WindReadingSerializer
    queryset = WindSpeedReadings.objects.all().order_by("date")
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WindReadingFilterSet
    ordering_fields = ["date", "anemometer"]


class SpeedStatsWithinRadiusView(APIView):
    @swagger_auto_schema(
        query_serializer=SpeedStatsWithinRadiusQuerySerializer,
        responses={200: SpeedStatsWithinRadiusResponseSerializer},
    )
    def get(self, request, *args, **kwargs):
        query_serializer = SpeedStatsWithinRadiusQuerySerializer(
            data=request.query_params
        )
        query_serializer.is_valid(raise_exception=True)

        anemometers_qs = self.get_anemometers_within_radius_qs(
            longitude=query_serializer.validated_data["lon"],
            latitude=query_serializer.validated_data["lat"],
            radius=query_serializer.validated_data["radius"],
        )

        readings = WindSpeedReadings.objects.filter(
            anemometer__in=anemometers_qs
        ).aggregate(
            min_speed=Round(Min("speed"), 2),
            max_speed=Round(Max("speed"), 2),
            mean_speed=Round(Avg("speed"), 2),
        )

        serializer = SpeedStatsWithinRadiusResponseSerializer(data=readings)
        serializer.is_valid()

        return Response(data=serializer.data)

    def get_anemometers_within_radius_qs(
        self, longitude: float, latitude: float, radius
    ) -> QuerySet:
        center = Point(longitude, latitude, srid=4326)
        anemometers_qs = Anemometer.objects.filter(
            coordinates__dwithin=(center, D(nm=radius))
        )
        return anemometers_qs
