from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


class APICounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        key = "counter"
        counter = cache.get(key, 0)
        counter += 1
        cache.set(key, counter, timeout=None)
        limit = 1000
        if counter > limit:
            return self.rate_limit_exceeded()
        # print(f"API has been called {counter} times")
        return None

    @staticmethod
    def rate_limit_exceeded(self):
        from django.http import JsonResponse
        response_data = {
            "error": "Too many requests",
            "message": "API rate limit exceeded, try again later."
        }
        return JsonResponse(response_data, status=429)