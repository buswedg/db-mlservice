import re

from django.shortcuts import redirect
from django.urls import reverse


class MaintenanceModeMiddleware:
    allowed_patterns = [
        r'^/admin/',
        r'^/static/',
        r'^/account/login/$',
        r'^/maintenance/$',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.pass_request(request):

            match = False
            for pattern in self.allowed_patterns:

                if re.compile(pattern).match(request.path):
                    match = True
                    break

            if not match:
                return redirect(reverse('maintenance'))

        return self.get_response(request)

    @staticmethod
    def pass_request(request):
        if request.user.is_authenticated:
            return request.user.is_active and request.user.is_staff

        return False
