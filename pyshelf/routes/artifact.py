import flask
from pyshelf.endpoint_decorators import decorators

artifact = flask.Blueprint("artifact", __name__)

@artifact.route("/", methods=["GET"], defaults={"path": ""})
@artifact.route("/<path:path>", methods=["GET"])
@decorators.foundation
def get_path(container, path):
    # TODO : This should list artifact resource links if it is a directory
    # or get the content of the artifact.
    with container.create_master_bucket_storage() as storage:
        stream = storage.get_artifact_stream(path)
        return flask.Response(stream)
