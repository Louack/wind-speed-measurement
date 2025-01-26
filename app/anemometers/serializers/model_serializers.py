from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from ..models import Anemometer, Tag


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
