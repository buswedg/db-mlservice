import logging
import os
from io import BytesIO
from uuid import uuid4

import requests
from django.core.files import File
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone

from .requests import get_agent_head_or_default

logger = logging.getLogger('custom')


def get_object_or_none(model, **kwargs):
    """
    Returns the object that matches the given keyword arguments or None if the object does not exist.
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def get_object_or_404_json(model, **kwargs):
    """
    Returns the object that matches the given keyword arguments or a JSON response with an error message if the object does not exist.
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return JsonResponse({'error': f"{model.__name__} not found."}, status=404)


def get_all_related_objects(model):
    """
    Returns all related objects for the given model.
    """
    return [
        f for f in model._meta.get_fields()
        if (f.one_to_many or f.one_to_one) and f.auto_created and not f.concrete
    ]


def get_all_related_m2m_objects(model):
    """
    Returns all related many-to-many objects for the given model.
    """
    return [
        f for f in model._meta.get_fields(include_hidden=True)
        if f.many_to_many and f.auto_created
    ]


def get_upload_path(instance, filename):
    """
    Returns the upload path for the given instance and filename.
    """
    path = os.path.join(
        instance._meta.app_label,
        instance._meta.model_name,
        timezone.now().strftime('%Y'),
        timezone.now().strftime('%m'),
        uuid4().hex,
        filename
    )

    return path


def check_storage_file_exists(file_path, storage=default_storage):
    """
    Checks whether a file exists in the storage or not.
    """
    return storage.exists(file_path)


def remove_storage_file_if_exists(file_path, storage=default_storage):
    """
    Removes the file from the storage if it exists.
    """
    if check_storage_file_exists(file_path, storage):
        try:
            storage.delete(file_path)
        except Exception as e:
            logger.error(e)


def get_url_as_field_file_or_false(url, filename):
    """
    Retrieves the file from the given URL and returns a file object or False if the request fails.
    """
    head = get_agent_head_or_default()
    req = requests.get(url, allow_redirects=True, stream=True, headers=head, timeout=10)
    req.raw.decode_content = True

    if req.status_code == 200:
        bytes_io = BytesIO()
        bytes_io.write(req.content)
        return File(bytes_io, name=filename)

    return False


def render_template(template_name, context={}):
    """
    Renders the given template with the given context and returns the rendered template.
    """
    return render_to_string(template_name, context=context)


def model_to_dict(instance, fields=None, exclude=None):
    """
    Returns a dictionary of model field names and their values for a model instance.
    """
    opts = instance._meta
    data = {}
    for f in opts.fields:
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data


def get_user_permission_level(user, obj):
    """
    Returns the permission level of the given user for the given object.
    """
    permission = None
    if user.is_superuser:
        permission = 'full'
    elif user.has_perm('app.change_%s' % obj.__class__.__name__.lower()):
        permission = 'edit'
    elif user.has_perm('app.view_%s' % obj.__class__.__name__.lower()):
        permission = 'view'
    return permission