import re

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.utils import timezone

from apps.log.models import VisitLog


class VisitLogMiddleware:
    # Adapted from django-user-visit
    # https://github.com/yunojuno/django-user-visit
    # version 0.4

    tracked_patterns = [
        r'^/api/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

        if not settings.VISIT_LOG_ENABLED:
            raise MiddlewareNotUsed

    def __call__(self, request):
        match = False
        for pattern in self.tracked_patterns:

            if re.compile(pattern).match(request.path):
                match = True
                break

        if match:
            visit_log = VisitLog.objects.build(request, timezone.now())
            if not VisitLog.objects.filter(hash=visit_log.hash).exists():
                visit_log.save()

        return self.get_response(request)
