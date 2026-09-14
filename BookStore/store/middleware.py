import logging
import time

logger = logging.getLogger("store")


class RequestLoggingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        # code before view
        logger.info(f"Request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}")

        # view
        response = self.get_response(request)

        # code after view
        duration = time.time() - start_time
        logger.info(
            f"Response: {request.method} {request.path} -> "
            f"{response.status_code} for {duration:.3f} seconds"
        )

        return response