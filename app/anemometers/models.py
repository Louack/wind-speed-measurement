from django.contrib.gis.db import models as gis_models
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
    )

    def __str__(self):
        return self.name


class Anemometer(gis_models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
    )
    coordinates = gis_models.PointField(geography=True, srid=4326)
    tags = models.ManyToManyField(to=Tag, related_name="anemometers", blank=True)

    def __str__(self):
        return self.name
