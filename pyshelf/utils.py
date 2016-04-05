from pyshelf.container import Container
import flask


def get_container():
    container = None
    if hasattr(flask, "g") and flask.g:
        container = getattr(flask.g, "container", None)
        if not container:
            container = Container(flask.current_app, flask.request)
            flask.g.container = container

    return container


def default_to_list(value):
    """
        Encapsulates non-list objects in a list for easy parsing.

        Args:
            value(object): value to be returned as is if it is a list or encapsulated in a list if not.
    """
    if not isinstance(value, list) and value is not None:
        value = [value]
    elif value is None:
        value = []

    return value
