from pyshelf.cloud.cloud_exceptions import CloudStorageException
from pyshelf.health_status import HealthStatus
from pyshelf.json_response import JsonResponse
from pyshelf.routes.artifact import artifact
import flask
import pyshelf.response_map as response_map

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
    h = app.health
    status = h.get_status()
    response = JsonResponse()
    response.headers["X-Status"] = status

    if "GET" == flask.request.method:
        body = {
            "status": status,
            "search": h.elasticsearch,
            "failingStorage": sorted(h.get_failing_ref_name_list()),
            "passingStorage": sorted(h.get_passing_ref_name_list())
        }

        response.set_data(body)

    if HealthStatus.OK != status:
        # Service Unavailable.
        response.status_code = 503

    return response
