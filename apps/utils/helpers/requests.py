import os
import random

import requests
from django.conf import settings


def is_ajax_request(request):
    """
    Returns True if the given request is an AJAX request.
    """
    return request.META.get('HTTP_X_REQUESTED_WITH') == "XMLHttpRequest"


def get_or_create_request_session_key(request):
    """
    Returns the session key for the given request.
    """
    if not request.session.exists(request.session.session_key):
        request.session.create()

    return request.session.session_key


def get_request_remote_addr(request):
    """
    Returns the remote address of the given request.
    """
    x_forwarded_for = request.headers.get('X-Forwarded-For', '')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]

    if not hasattr(request, 'META'):
        return ''

    return request.META.get('REMOTE_ADDR', '')


def get_request_ua_string(request):
    """
    Returns the user agent string of the given request.
    """
    if not hasattr(request, 'META'):
        return ''

    return request.META.get('HTTP_USER_AGENT', '')


def get_random_agent_or_false():
    """
    Returns a random user agent string from the user agent list file or False if the file does not exist.
    """
    agent_file_path = "apps/utils/data/user_agent_list.txt"
    f = os.path.join(settings.BASE_DIR, agent_file_path)
    agent = False

    if os.path.exists(f):
        with open(f, 'r') as f:
            content = f.read(1)

            if content:
                lines = f.readlines()
                agent = str(random.choice(lines)).replace('\n', '')

    return agent


def get_agent_head_or_default():
    """
    Returns the default user agent header or a random user agent header.
    """
    head = {
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    agent = get_random_agent_or_false()
    if agent:
        head['User-Agent'] = agent

    return head


def get_url_head_or_false(url):
    """
    Returns the head of the given URL or False if the request fails.
    """
    head = get_agent_head_or_default()
    req = requests.head(url, allow_redirects=True, headers=head, timeout=5)
    if req.status_code == requests.codes.ok:
        return req

    return False


def get_client_ip(request):
    """
    Returns the client's IP address.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
