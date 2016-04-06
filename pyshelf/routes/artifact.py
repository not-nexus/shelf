from flask import request, Blueprint
from pyshelf.endpoint_decorators import decorators
import pyshelf.response_map as response_map
import json

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
    with container.create_bucket_storage() as storage:
        file = request.files['file']
        storage.upload_artifact(path, file)
        response = response_map.create_201()
        response.headers["Location"] = container.request.path

    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta", methods=["GET"])
@decorators.foundation
def get_artifact_meta_route(container, bucket_name, path):
    return get_artifact_meta(container, bucket_name, path)


def get_artifact_meta(container, bucket_name, path):
    return response_map.create_200(container.metadata.manager.metadata)


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta", methods=["PUT"])
@decorators.foundation_headers
def update_artifact_meta(container, bucket_name, path):
    data = json.loads(request.data)
    manager = container.metadata.manager
    manager.try_update(data)
    response = get_artifact_meta(container, bucket_name, path)
    response.headers["Location"] = container.request.path
    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta/<item>", methods=["GET"])
@decorators.foundation
def get_metadata_property_route(container, bucket_name, path, item):
    return get_metadata_property(container, bucket_name, path, item)


def get_metadata_property(container, bucket_name, path, item):
    manager = container.metadata.manager
    data = manager.metadata.get(item)
    if None is data:
        response = response_map.create_404()
    else:
        response = response_map.create_200(data)

    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta/<item>", methods=["POST", "PUT"])
@decorators.foundation_headers
def create_metadata_property(container, bucket_name, path, item):
    data = json.loads(request.data)
    manager = container.metadata.manager
    exists = (item in manager.metadata)
    result = None

    if request.method == "PUT":
        result = manager.try_update_property(item, data)
    else:
        result = manager.try_create_property(item, data)

    if result.success:
        response = get_metadata_property(container, bucket_name, path, item)
        if not exists:
            response.status_code = 201

        response.headers["Location"] = container.request.path
    else:
        response = response_map.map_metadata_result_errors(result)

    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta/<item>", methods=["DELETE"])
@decorators.foundation
def delete_metadata_property(container, bucket_name, path, item):
    manager = container.metadata.manager
    result = manager.try_delete_property(item)
    response = None
    if result.success:
        response = response_map.create_204()
    else:
        response = response_map.map_metadata_result_errors(result)

    return response


@artifact.route("/<bucket_name>/artifact/_search", methods=["POST"])
@decorators.foundation
def root_search(container, bucket_name):
    response = search(container)
    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_search", methods=["POST"])
@decorators.foundation
def path_search(container, bucket_name, path):
    response = search(container)
    return response


def search(container):
    """
        Does a search with the given criteria.

        Args:
            container(pyshelf.container.Container)

        Returns:
            Flask response
    """
    criteria = request.get_json(force=True)
    container.search_portal.search(criteria)

    if container.context.has_error():
        response = response_map.map_context_error(container.context)
    else:
        response = container.context_response_mapper.to_response(status_code=204)

    return response
