import datetime as dt
import logging
import random
import string

import numpy as np

_SHORT_UUID_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def strp_dt_or_nan(string, fmt):
    """
    Returns a datetime object from the given string and format, or np.nan if an error occurs.
    """
    try:
        return dt.datetime.strptime(string, fmt)
    except ValueError as e:
        logging.error(e)

    return np.nan


def strp_time_or_nan(string, fmt):
    """
    Returns a time object from the given string and format, or np.nan if an error occurs.
    """
    try:
        return dt.datetime.strptime(string, fmt).time()
    except ValueError as e:
        logging.error(e)

    return np.nan


def snake_to_camel(snake):
    """
    Returns a camel case string from the given snake case string.
    """
    first, *rest = snake.split('_')
    return first + ''.join(word.capitalize() for word in rest)


def generate_random_string(length):
    """
    Generates a random string of the given length.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def uuid_to_shortuuid(uuid, length=16):
    """
    Converts a UUID to a short UUID.
    """
    hex_str = uuid.hex
    hex_int = int(hex_str, length)
    res_str = ""
    while hex_int > 0:
        hex_int, remainder = divmod(hex_int, len(_SHORT_UUID_ALPHABET))
        res_str = _SHORT_UUID_ALPHABET[remainder] + res_str
    return res_str