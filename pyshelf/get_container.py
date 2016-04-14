from pyshelf.container import Container
import flask
"""
    This module is purposfully by itself in this file.  The reason for this
    is because it imports Container and Container imports EVERYTHING ELSE.
    python does not do well with recursive imports but likely any
    "utils" file will be imported in many different modules.
"""


def get_container():
    container = None
    if hasattr(flask, "g") and flask.g:
        container = getattr(flask.g, "container", None)
        if not container:
            container = Container(flask.current_app, flask.request)
            flask.g.container = container

    return container
