from flask import request, Blueprint, Response
from pyshelf.endpoint_decorators import decorators
from pyshelf.cloud.cloud_exceptions import CloudStorageException
from pyshelf.cloud.metadata_mapper import MetadataMapper
import pyshelf.response_map as response_map
import json

artifact = Blueprint("artifact", __name__)


@artifact.route("/", methods=["GET"], defaults={"path": "/"})
@artifact.route("/<path:path>", methods=["GET"])
@decorators.foundation
def get_path(container, path):
    try:
        response = container.artifact_list_manager.get_artifact(path)
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
        meta_mapper = MetadataMapper(container, path)
        return response_map.create_200(meta_mapper.get_metadata())
    except CloudStorageException as e:
        return response_map.map_exception(e)


@artifact.route("/<path:path>/_meta", methods=["PUT"])
@decorators.foundation_headers
def update_artifact_meta(container, path):
    try:
        meta_mapper = MetadataMapper(container, path)
        data = json.loads(request.data)
        meta_mapper.set_metadata(data)
        response = get_artifact_meta(path)
        response.status_code = 201
        return response
    except CloudStorageException as e:
        return response_map.map_exception(e)


@artifact.route("/<path:path>/_meta/<item>", methods=["GET"])
@decorators.foundation
def get_metadata_item(container, path, item):
    try:
        meta_mapper = MetadataMapper(container, path)
        metadata = meta_mapper.get_metadata(item)
        return response_map.create_200(metadata)
    except CloudStorageException as e:
        return response_map.map_exception(e)


@artifact.route("/<path:path>/_meta/<item>", methods=["POST", "PUT"])
@decorators.foundation_headers
def create_metadata_item(container, path, item):
    try:
        data = json.loads(request.data)
        meta_mapper = MetadataMapper(container, path)

        if not meta_mapper.item_exists(item):
            meta_mapper.set_metadata(data, item)
            response = get_metadata_item(path, item)
            response.status_code = 201
        elif meta_mapper.item_exists(item) and request.method == "PUT":
            success = meta_mapper.set_metadata(data, item)
            response = get_metadata_item(path, item)
        else:
            response = response_map.create_403()
        return response

    except CloudStorageException as e:
        return response_map.map_exception(e)


@artifact.route("/<path:path>/_meta/<item>", methods=["DELETE"])
@decorators.foundation
def delete_metadata_item(container, path, item):
    try:
        meta_mapper = MetadataMapper(container, path)
        meta_mapper.remove_metadata(item)
        return response_map.create_204()
    except CloudStorageException as e:
        return response_map.map_exception(e)
