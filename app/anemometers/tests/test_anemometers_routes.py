from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Anemometer


class AnemometerAPITestCase(APITestCase):
    def setUp(self):
        call_command("loaddata", "fixtures.json")
        self.user = User.objects.first()
        self.client.force_authenticate(user=self.user)

    def test_list_anemometers_anonymous(self):
        self.client.force_authenticate(user=None)
        url = reverse("anemometers-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_anemometers(self):
        url = reverse("anemometers-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["results"]["features"]) == 5

    @freeze_time("2025-01-27 0:00:00")
    def test_retrieve_anemometer(self):
        obj = Anemometer.objects.get(id=1)
        url = reverse("anemometers-detail", kwargs={"pk": obj.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": 1,
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-73.985428, 40.748817]},
            "properties": {
                "name": "New York - Empire State Building",
                "tags": ["USA"],
                "last_day_mean_speed": 59.0,
                "last_week_mean_speed": 57.77,
            },
        }

    def test_delete_anemometer(self):
        obj = Anemometer.objects.get(id=1)
        url = reverse("anemometers-detail", kwargs={"pk": obj.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_post_anemometers(self):
        url = reverse("anemometers-list")
        data = {
            "name": "new",
            "coordinates": {"type": "Point", "coordinates": [0, 0]},
            "tags_to_link": [
                "New",
            ],
        }
        response = self.client.post(path=url, data=data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "id": 6,
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [0.0, 0.0]},
            "properties": {"name": "new", "tags": ["New"]},
        }

    def test_update_anemometer(self):
        obj = Anemometer.objects.get(id=1)
        name = obj.name
        url = reverse("anemometers-detail", kwargs={"pk": obj.pk})
        data = {"name": "updated"}
        response = self.client.patch(path=url, data=data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["properties"]["name"] == "updated"
        assert response.json()["properties"]["name"] != name

    def test_filter_anemometers_by_usa_tag(self):
        """
        Of the 5 anemometers fixtures, 4 are wearing the USA tag.
        """
        url = reverse("anemometers-list")
        response = self.client.get(path=url, data={"tag": "USA"})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 4

    def test_daily_mean_speeds(self):
        obj = Anemometer.objects.get(id=5)
        url = reverse("anemometers-get-daily-mean-speeds", kwargs={"pk": obj.pk})

        response = self.client.get(path=url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["results"] == [
            {"day": "2025-01-22T00:00:00Z", "mean_speed": 53.6},
            {"day": "2025-01-18T00:00:00Z", "mean_speed": 15.0},
            {"day": "2025-01-15T00:00:00Z", "mean_speed": 20.0},
            {"day": "2025-01-04T00:00:00Z", "mean_speed": 30.0},
            {"day": "2025-01-03T00:00:00Z", "mean_speed": 30.0},
        ]

    def test_weekly_mean_speeds(self):
        obj = Anemometer.objects.get(id=5)
        url = reverse("anemometers-get-weekly-mean-speeds", kwargs={"pk": obj.pk})

        response = self.client.get(path=url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["results"] == [
            {"week": "2025-01-20T00:00:00Z", "mean_speed": 53.6},
            {"week": "2025-01-13T00:00:00Z", "mean_speed": 16.25},
            {"week": "2024-12-30T00:00:00Z", "mean_speed": 30.0},
        ]
