from rest_framework import serializers


class SpeedStatsWithinRadiusResponseSerializer(serializers.Serializer):
    min_speed = serializers.FloatField(help_text="speed in knots")
    max_speed = serializers.FloatField(help_text="speed in knots")
    mean_speed = serializers.FloatField(help_text="speed in knots")
