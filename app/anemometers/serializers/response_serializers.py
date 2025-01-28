from rest_framework import serializers


class DailyMeanSpeedsResponseSerializer(serializers.Serializer):
    day = serializers.DateTimeField(
        help_text="The day on which the mean speed was computed"
    )
    mean_speed = serializers.FloatField(help_text="speed in knots")


class WeeklyMeanSpeedsResponseSerializer(serializers.Serializer):
    week = serializers.DateTimeField(
        help_text="The week starting day on which the mean speed was computed"
    )
    mean_speed = serializers.FloatField(help_text="speed in knots")


class SpeedStatsWithinRadiusResponseSerializer(serializers.Serializer):
    min_speed = serializers.FloatField(help_text="speed in knots")
    max_speed = serializers.FloatField(help_text="speed in knots")
    mean_speed = serializers.FloatField(help_text="speed in knots")
