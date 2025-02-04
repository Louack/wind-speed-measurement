from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from core.cache import clear_anemometer_cache

from .models import WindSpeedReadings


@receiver(post_save, sender=WindSpeedReadings)
@receiver(post_delete, sender=WindSpeedReadings)
def empty_cache(sender, instance, **kwargs):
    clear_anemometer_cache(instance.anemometer_id)
