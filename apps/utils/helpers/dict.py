def get_dict_item_or_default(dic, idx, default=None):
    """
    Returns the item of the given dictionary with the given index or the default value if the index does not exist.
    """
    try:
        return dic[idx]
    except IndexError:
        return default


def del_dict_item_if_exists(dic, key):
    """
    Deletes the item of the given dictionary with the given key if it exists.
    """
    try:
        del dic[key]
    except KeyError:
        pass