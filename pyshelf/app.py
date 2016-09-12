import flask
from pyshelf.routes.artifact import artifact
import pyshelf.response_map as response_map
from pyshelf.cloud.cloud_exceptions import CloudStorageException

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
