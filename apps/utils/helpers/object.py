def resolve_obj_or_none(obj, *attrs):
    """
    Returns the object that matches the given attributes or None if the object does not exist.
    """
    for attr in attrs:
        try:
            obj = getattr(obj, attr, None)
        except (TypeError, AttributeError):
            return None

    return obj


def has_all_attr(obj, *attrs):
    """
    Returns True if the given object has all the given attributes.
    """
    return all(hasattr(obj, attr) for attr in attrs)


def has_any_attr(obj, *attrs):
    """
    Returns True if the given object has any of the given attributes.
    """
    return any(hasattr(obj, attr) for attr in attrs)


def cast_obj_to_iter(obj):
    """
    Casts the given object to an iterable object.
    """
    try:
        return iter(obj)
    except TypeError:
        pass

    return iter([obj])


def cast_obj_to_list(obj):
    """
    Casts the given object to a list.
    """
    try:
        return list(obj)
    except TypeError:
        pass

    return [obj]
