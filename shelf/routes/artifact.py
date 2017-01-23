from flask import request, Blueprint
from shelf.endpoint_decorators import decorators
import shelf.response_map as response_map
from shelf.error_code import ErrorCode
import requests

artifact = Blueprint("artifact", __name__)


@artifact.route("/<bucket_name>/artifact/", methods=["GET", "HEAD"], defaults={"path": "/"})
@artifact.route("/<bucket_name>/artifact/<path:path>", methods=["GET", "HEAD"])
@decorators.foundation
def get_path(container, bucket_name, path):
    """
        Flask automatically maps HEAD requests to GET endpoint. We added it to the list of methods
        to be more explicit. We handle it differently to avoid initiating the downloading of an
        artifact as it is unnecessary.
    """
    content = None
    status_code = 204

    if container.request.method == "HEAD":
        container.artifact_manager.assign_artifact_links(path)
    else:
        content = container.artifact_manager.get_artifact(path)

    if content:
        status_code = 200

    response = container.context_response_mapper.to_response(content, status_code)

    return response


@artifact.route("/<bucket_name>/artifact/<path:path>", methods=["POST"])
@decorators.foundation
def upload_artifact(container, bucket_name, path):
    file_storage = request.files['file']
    container.artifact_manager.upload_artifact(path, file_storage)
    response = response_map.create_201()
    response = container.context_response_mapper.to_response(response.data, response.status_code)
    response.headers["Location"] = container.request.path

    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta", methods=["GET", "HEAD"])
@decorators.foundation
def get_artifact_meta_route(container, bucket_name, path):
    return get_artifact_meta(container, bucket_name, path)


def get_artifact_meta(container, bucket_name, path):
    container.link_manager.assign_single(path)
    metadata = container.metadata.manager.metadata
    response = container.context_response_mapper.to_response(metadata, 200)
    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_meta", methods=["PUT"])
@decorators.foundation
@decorators.validate_request("schemas/request-metadata.json")
def update_artifact_meta(container, bucket_name, path, data):
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
@decorators.foundation
@decorators.validate_request("schemas/request-metadata-property.json")
def create_metadata_property(container, bucket_name, path, item, data):
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
@decorators.validate_request("schemas/search-request-criteria.json", {})
def root_search(container, bucket_name, data):
    response = search(container, data)

    return response


@artifact.route("/<bucket_name>/artifact/<path:path>/_search", methods=["POST"])
@decorators.foundation
@decorators.validate_request("schemas/search-request-criteria.json", {})
def path_search(container, bucket_name, path, data):
    response = search(container, data)

    return response


def search(container, criteria=None):
    """
        Does a search with the given criteria.

        Args:
            container(shelf.container.Container)
            criteria(dict | None)

        Returns:
            Flask response
    """
    try:
        container.search_portal.search(criteria)
    except requests.ConnectionError as ex:
        container.app.health.elasticsearch = False
        raise ex

    container.app.health.elasticsearch = True

    if container.context.has_error():
        response = response_map.map_context_error(container.context)
    else:
        response = container.context_response_mapper.to_response(status_code=204)

    return response
