from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class APICounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        key="counter"
        counter = cache.get(key, 0)
        counter += 1

        # Store the updated counter back in the cache
        cache.set(key, counter, timeout=None)  # No timeout for the key

        # Optional: Handle rate-limiting
        limit = 1000  # Example request limit
        if counter > limit:
            return self.rate_limit_exceeded()

        print(f"API has been called {counter} times")
        return None  # Continue processing the request

    def rate_limit_exceeded(self):
        from django.http import JsonResponse
        response_data = {
            "error": "Too many requests",
            "message": "API rate limit exceeded, try again later."
        }
        return JsonResponse(response_data, status=429)