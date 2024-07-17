def chunk_list(lst, size):
    """
    Splits a list into smaller sub-lists of the given size.
    """
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def flatten_list(lst):
    """
    Flattens a list of lists into a single list.
    """
    return [item for sublist in lst for item in sublist]


def remove_list_duplicates(lst):
    """
    Removes duplicates from a list while preserving the order of the remaining items.
    """
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]
