from django.contrib.gis.db import models as gis_models
from django.core.validators import MaxValueValidator, MinValueValidator
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


class WindSpeedReadings(models.Model):
    anemometer = models.ForeignKey(
        to=Anemometer, on_delete=models.CASCADE, related_name="wind_readings"
    )
    speed = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        help_text="speed in knots",
    )
    date = models.DateTimeField()
