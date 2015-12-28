from flask import request, Blueprint, Response
from pyshelf.endpoint_decorators import decorators
from pyshelf.cloud.cloud_exceptions import CloudStorageException
import pyshelf.response_map as response_map

artifact = Blueprint("artifact", __name__)


@artifact.route("/", methods=["GET"], defaults={"path": ""})
@artifact.route("/<path:path>", methods=["GET"])
@decorators.foundation
def get_path(container, path):
    # TODO : This should list artifact resource links if it is a directory
    # or get the content of the artifact.
    try:
        with container.create_master_bucket_storage() as storage:
            stream = storage.get_artifact(path)
            response = Response(stream)
            response.headers["Content-Type"] = stream.headers["content-type"]
            return response
    except CloudStorageException as e:
        return response_map.map_exception(e)


@artifact.route("/", methods=["POST"], defaults={"path": ""})
@artifact.route("/<path:path>", methods=["POST"])
@decorators.foundation_headers
def create_artifact(container, path):
    try:
        with container.create_master_bucket_storage() as storage:
            file = request.files['file']
            storage.upload_artifact(path, file)
            return response_map.create_201()
    except CloudStorageException as e:
        return response_map.map_exception(e)


@artifact.route("/<path:path>/_meta", methods=["GET"])
@decorators.foundation
def get_artifact_meta(container, path):
    try:
        with container.create_master_bucket_storage() as storage:
            meta = storage.get_artifact_metadata(path)
            return response_map.create_200(meta)
    except CloudStorageException as e:
        return response_map.map_exception(e)


@artifact.route("/<path:path>/_meta", methods=["PUT"])
@decorators.foundation_headers
def update_artifact_meta(container, path):
    try:
        with container.create_master_bucket_storage() as storage:
            storage.set_artifact_meta(path, request.data)
            return response_map.create_201() 
    except CloudStorageException as e:
        return response_map.map_exception(e)
