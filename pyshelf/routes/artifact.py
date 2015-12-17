import flask
from pyshelf.endpoint_decorators import decorators

artifact = flask.Blueprint("artifact", __name__)

@artifact.route("/", methods=["GET"], defaults={"path": ""})
@artifact.route("/<path:path>", methods=["GET"])
@decorators.foundation
def get_path(container, path):
    # TODO : This should list artifact resource links if it is a directory
    # or get the content of the artifact.
    return flask.Response("Path was " + path)
    
