from datetime import datetime, timedelta

from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from ..models import Anemometer, Tag, WindSpeedReadings


class AnemometerSerializer(GeoFeatureModelSerializer):
    tags_to_link = serializers.ListField(
        child=serializers.CharField(max_length=64), write_only=True, required=False
    )
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Anemometer
        geo_field = "coordinates"
        fields = ("id", "name", "coordinates", "tags", "tags_to_link")

    def get_tags(self, obj):
        return obj.tags.all().values_list("name", flat=True)

    def validate_coordinates(self, value):
        longitude, latitude = value.coords
        if not (-180 <= longitude <= 180):
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        if not (-90 <= latitude <= 90):
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

    def create(self, validated_data):
        tag_names = validated_data.pop("tags_to_link", [])
        anemometer = Anemometer.objects.create(**validated_data)
        tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
        anemometer.tags.set(tags)
        return anemometer

    def update(self, instance, validated_data):
        tag_names = validated_data.pop("tags_to_link", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
        instance.tags.set(tags)

        return instance


class WindReadingSerializer(serializers.ModelSerializer):
    anemometer_to_link = serializers.CharField(max_length=64, write_only=True)
    anemometer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WindSpeedReadings
        fields = ("id", "anemometer", "anemometer_to_link", "speed", "date")

    def get_anemometer(self, obj):
        return obj.anemometer.name

    def create(self, validated_data):
        anemometer_name = validated_data.pop("anemometer_to_link")
        try:
            anemometer = Anemometer.objects.get(name=anemometer_name)
        except Anemometer.DoesNotExist:
            raise serializers.ValidationError(
                "Anemometer with this name does not exist"
            )

        validated_data["anemometer"] = anemometer
        reading = WindSpeedReadings.objects.create(**validated_data)

        return reading

    def update(self, instance, validated_data):
        anemometer_name = validated_data.pop("anemometer_to_link", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if anemometer_name:
            try:
                anemometer = Anemometer.objects.get(name=anemometer_name)
                instance.anemometer = anemometer
            except Anemometer.DoesNotExist:
                raise serializers.ValidationError(
                    "Anemometer with this name does not exist"
                )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def validate_speed(self, value):
        return round(value, 2)


class AnemometerRetrieveSerializer(GeoFeatureModelSerializer):
    daily_mean_speed = serializers.SerializerMethodField(
        allow_null=True, help_text="speed in knots"
    )
    weekly_mean_speed = serializers.SerializerMethodField(
        allow_null=True, help_text="speed in knots"
    )
    tags = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Anemometer
        geo_field = "coordinates"
        fields = (
            "id",
            "name",
            "coordinates",
            "tags",
            "daily_mean_speed",
            "weekly_mean_speed",
        )

    def get_tags(self, obj):
        return obj.tags.all().values_list("name", flat=True)

    def get_daily_mean_speed(self, anemometer):
        last_day = datetime.now() - timedelta(days=1)
        mean_speed = (
            anemometer.wind_readings.filter(date__gte=last_day)
            .aggregate(mean_speed=Round(Avg("speed"), 2))
            .get("mean_speed")
        )
        return mean_speed

    def get_weekly_mean_speed(self, anemometer):
        last_week = datetime.now() - timedelta(weeks=1)
        mean_speed = (
            anemometer.wind_readings.filter(date__gte=last_week)
            .aggregate(mean_speed=Round(Avg("speed"), 2))
            .get("mean_speed")
        )
        return mean_speed
