from shelf.cloud.cloud_exceptions import CloudStorageException
from shelf.health_status import HealthStatus
from shelf.json_response import JsonResponse
from shelf.routes.artifact import artifact
from shelf.endpoint_decorators import decorators
from shelf.link_title import LinkTitle
import flask
import shelf.response_map as response_map

app = flask.Flask(__name__)
app.register_blueprint(artifact)


@app.errorhandler(Exception)
@app.errorhandler(CloudStorageException)
def generic_exception_handler(error):
    """
        Prevents Exceptions flying all around the place.
    """
    response = None
    app.logger.exception(error)
    response = response_map.map_exception(error)

    return response


@app.after_request
def format_response(response):
    response.headers["Cache-Control"] = "no-cache"

    if response.status_code == 404:
        response = response_map.create_404()

    if response.headers["Content-Type"] == "application/json":
        data = response.get_data()
        data += "\n"
        response.set_data(data)
    return response


@app.route("/health", methods=["HEAD", "GET"])
def health():
    # TODO: I've removed lots of functionality from the health
    # check due to lack of time and shared memory issues.
    response = JsonResponse()
    status = HealthStatus.OK
    response.headers["X-Status"] = status

    if "GET" == flask.request.method:
        body = {
            "status": HealthStatus.OK,
        }

        response.set_data(body)

    return response


@app.route("/", methods=["GET"])
@decorators.injectcontainer
@decorators.logtraffic
def list_shelves(container):
    auth = container.request.headers.get("Authorization")

    if auth:
        bucket_list = container.list_shelves_manager.list(auth)
        link_list = []

        for bucket in bucket_list:
            path = flask.url_for("artifact.get_path", bucket_name=bucket)
            link_list.append({
                "type": "collection",
                "title": LinkTitle.ARTIFACT_ROOT,
                "path": path
            })

        link_list = container.link_mapper.to_response(link_list)
        response = JsonResponse()

        for link in link_list:
            response.headers.add("Link", link)

        response.set_data(bucket_list)
    else:
        response = response_map.create_401()

    return response
