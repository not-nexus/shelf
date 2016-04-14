def default_to_list(value):
    """
        Ensures non-list objects are add to a list for easy parsing.

        Args:
            value(object): value to be returned as is if it is a list or encapsulated in a list if not.
    """
    if not isinstance(value, list) and value is not None:
        value = [value]
    elif value is None:
        value = []

    return value
