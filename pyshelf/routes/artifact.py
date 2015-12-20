import flask
from pyshelf.endpoint_decorators import decorators
from pyshelf.cloud.cloud_exceptions import ArtifactNotFoundError, BucketNotFoundError
import pyshelf.response_map as response_map

artifact = flask.Blueprint("artifact", __name__)


@artifact.route("/", methods=["GET"], defaults={"path": ""})
@artifact.route("/<path:path>", methods=["GET"])
@decorators.foundation
def get_path(container, path):
    # TODO : This should list artifact resource links if it is a directory
    # or get the content of the artifact.
    try:
        with container.create_master_bucket_storage() as storage:
            stream = storage.get_artifact(path)
            response = flask.Response(stream)
            response.headers["Content-Type"] = stream.headers["content-type"]
            return response
    except (ArtifactNotFoundError, BucketNotFoundError) as e:
        if isinstance(e, ArtifactNotFoundError):
            return response_map.create_404()
        if isinstance(e, BucketNotFoundError):
            return response_map.create_500()
