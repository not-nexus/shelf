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
