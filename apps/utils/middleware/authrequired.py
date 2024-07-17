import re

from django.shortcuts import redirect
from django.urls import reverse


class AuthRequiredMiddleware:
    allowed_patterns = [
        r'^/admin/',
        r'^/static/',
        r'^/account/login/$',
        r'^/account/password-reset/$',
        r'^/account/password-reset-done/$',
        r'^/account/password-reset-complete/$',
        r'^/account/password-change-done/$',
        r'^/account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,36})/$',
        r'^/account/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/set-password/$'
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
                return redirect(reverse('account:login'))

        return self.get_response(request)

    @staticmethod
    def pass_request(request):
        return request.user.is_authenticated
