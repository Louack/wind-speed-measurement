from functools import wraps

from django.core.cache import cache
from rest_framework.response import Response


def cache_response(timeout: int = 600):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            cache_key = f"{request.get_full_path()}"
            cached_data = cache.get(cache_key)

            if cached_data:
                return Response(cached_data)

            response = func(self, request, *args, **kwargs)

            cache.set(cache_key, response.data, timeout=timeout)

            return response

        return wrapper

    return decorator


def clear_anemometer_cache(anemometer_id):
    uris = [
        f"/anemometers/{anemometer_id}",
        f"/anemometers/{anemometer_id}/mean/daily",
        f"/anemometers/{anemometer_id}/mean/weekly",
    ]
    for uri in uris:
        cache.delete(uri)
