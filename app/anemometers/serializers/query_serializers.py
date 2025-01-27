from rest_framework import serializers


class SpeedStatsWithinRadiusQuerySerializer(serializers.Serializer):
    lon = serializers.FloatField(
        min_value=-180, max_value=180, help_text="Longitude of the center point"
    )
    lat = serializers.FloatField(
        min_value=-90, max_value=90, help_text="Latitude of the center point"
    )
    radius = serializers.FloatField(
        min_value=0, max_value=500, help_text="radius in nautical miles"
    )
