from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from sentry_sdk import configure_scope


class SentryUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        if not settings.SENTRY_ENABLED:
            raise MiddlewareNotUsed

    def __call__(self, request):
        with configure_scope() as scope:
            if request.user.is_authenticated:
                scope.user = {
                    "id": request.user.id,
                }
        response = self.get_response(request)
        return response
