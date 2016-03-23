from flask import request, Blueprint
from pyshelf.endpoint_decorators import decorators
from pyshelf.cloud.metadata_mapper import MetadataMapper
import pyshelf.response_map as response_map
import json
from pyshelf.json_response import JsonResponse

artifact = Blueprint("artifact", __name__)


@artifact.route("/<bucket_name>/artifact/", methods=["GET"], defaults={"path": "/"})
@artifact.route("/<bucket_name>/artifact/<path:path>", methods=["GET"])
@decorators.foundation
def get_path(container, bucket_name, path):
    stream = container.artifact_list_manager.get_artifact(path)
    status_code = 204
    if stream:
        status_code = 200

    response = container.context_response_mapper.to_response(stream, status_code)
    return response


@artifact.route("/<bucket_name>/artifact/<path:path>", methods=["POST"])
@decorators.foundation_headers
def create_artifact(container, bucket_name, path):
    response = None
    with container.create_master_bucket_storage() as storage:
        file = request.files['file']
        storage.upload_artifact(path, file)
        response = response_map.create_201()
        response.headers["Location"] = container.request.path

    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta", methods=["GET"])
@decorators.foundation
def get_artifact_meta(container, bucket_name, path):
    meta_mapper = MetadataMapper(container, path)
    return response_map.create_200(meta_mapper.get_metadata())


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta", methods=["PUT"])
@decorators.foundation_headers
def update_artifact_meta(container, bucket_name, path):
    meta_mapper = MetadataMapper(container, path)
    data = json.loads(request.data)
    meta_mapper.set_metadata(data)
    response = JsonResponse()
    response.set_data(meta_mapper.metadata)
    response.status_code = 201
    response.headers["Location"] = container.request.path
    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta/<item>", methods=["GET"])
@decorators.foundation
def get_metadata_item(container, bucket_name, path, item):
    meta_mapper = MetadataMapper(container, path)
    metadata = meta_mapper.get_metadata(item)
    return response_map.create_200(metadata)


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta/<item>", methods=["POST", "PUT"])
@decorators.foundation_headers
def create_metadata_item(container, bucket_name, path, item):
    data = json.loads(request.data)
    meta_mapper = MetadataMapper(container, path)

    if not meta_mapper.item_exists(item) or request.method == "PUT":
        meta_mapper.set_metadata(data, item)
        meta = meta_mapper.get_metadata(item)
        response = response_map.create_200(meta)
        response.headers["Location"] = container.request.path
    else:
        response = response_map.create_403()
    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta/<item>", methods=["DELETE"])
@decorators.foundation
def delete_metadata_item(container, bucket_name, path, item):
    meta_mapper = MetadataMapper(container, path)
    meta_mapper.remove_metadata(item)
    return response_map.create_204()
