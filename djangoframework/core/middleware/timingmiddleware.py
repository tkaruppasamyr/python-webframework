import time
from django.utils.decorators import sync_and_async_middleware

@sync_and_async_middleware
def AsyncTimingMiddleware(get_response):

    if callable(get_response):
        # Django decides sync or async automatically

        async def async_middleware(request):
            start_time = time.perf_counter()

            response = await get_response(request)

            duration = time.perf_counter() - start_time
            print(f"Duration: {duration}")

            response["X-Response-Time"] = f"{duration:.6f}"
            return response

        def sync_middleware(request):
            start_time = time.perf_counter()

            response = get_response(request)

            duration = time.perf_counter() - start_time
            print(f"Duration: {duration}")

            response["X-Response-Time"] = f"{duration:.6f}"
            return response

        return async_middleware if hasattr(get_response, "__await__") else sync_middleware