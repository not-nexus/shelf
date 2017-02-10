from shelf.cloud.cloud_exceptions import CloudStorageException
from shelf.health_status import HealthStatus
from shelf.json_response import JsonResponse
from shelf.routes.artifact import artifact
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
