import os


def check_file_exists(file_path):
    """
    Checks whether a file exists or not.
    """
    return os.path.exists(file_path)


def remove_file_if_exists(file_path):
    """
    Removes the file if it exists.
    """
    if check_file_exists(file_path):
        with open(file_path, 'w') as f:
            os.remove(file_path)


def rename_file(file_path, prefix=None, ext=None):
    """
    Renames the file with the given prefix and extension.
    """
    basename = os.path.basename(file_path)
    if prefix:
        basename = prefix + basename
    if ext:
        basename = os.path.splitext(basename)[0] + ext

    return basename


def filter_by_extensions(item_list, endings):
    """
    Filters the given list of items by the given extensions.
    """
    if not item_list:
        return []

    if not endings:
        return item_list

    return [item for item in item_list if not any(item.lower().endswith(e) for e in endings)]
