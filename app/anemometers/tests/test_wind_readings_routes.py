from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Anemometer
from ..views import SpeedStatsWithinRadiusView


class WindReadingsAPITestCase(APITestCase):
    def setUp(self):
        call_command("loaddata", "fixtures.json")
        self.user = User.objects.first()
        self.client.force_authenticate(user=self.user)

    def test_post_readings(self):
        url = reverse("readings-list")
        data = {
            "anemometer_to_link": "New York - Empire State Building",
            "speed": 10.356,
            "date": "2025-01-01T00:00",
        }
        response = self.client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "id": 21,
            "anemometer": "New York - Empire State Building",
            "speed": 10.36,
            "date": "2025-01-01T00:00:00Z",
        }

    def test_list_readings_per_anemometers(self):
        obj = Anemometer.objects.get(id=1)
        url = reverse("anemometers-get-readings", kwargs={"pk": obj.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "count" in response.json()
        assert response.json()["results"] == [
            {
                "id": 2,
                "anemometer": "New York - Empire State Building",
                "speed": 72.4,
                "date": "2025-01-26T15:00:00Z",
            },
            {
                "id": 1,
                "anemometer": "New York - Empire State Building",
                "speed": 45.6,
                "date": "2025-01-26T10:00:00Z",
            },
            {
                "id": 3,
                "anemometer": "New York - Empire State Building",
                "speed": 55.3,
                "date": "2025-01-25T18:00:00Z",
            },
        ]

    def test_filter_readings_by_usa_tag(self):
        """
        Of the 15 anemometers fixtures, 12 are linked to anemometers wearing the USA tag.
        """
        url = reverse("readings-list")
        response = self.client.get(path=url, data={"tag": "USA"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 12

    def test_get_anemometers_within_radius_method(self):
        """
        latitude 40 and longitude -74 are the NYC coordinates.
        Within a 100 nm radius we should only retrieve the 3 NYC anemometers fixtures
        """
        method = SpeedStatsWithinRadiusView.get_anemometers_within_radius_qs
        result = method(self, latitude=40, longitude=-74, radius=100)

        assert result.count() == 3

    @freeze_time("2025-01-27 0:00:00")
    def test_get_readings_within_radius_stats_route(self):
        url = reverse("readings-radius-stats")
        response = self.client.get(
            path=url, data={"lon": -74, "lat": 40, "radius": 100}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "min_speed": 40.3,
            "max_speed": 78.9,
            "mean_speed": 58.23,
        }
