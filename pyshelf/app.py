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
    if isinstance(error, CloudStorageException):
        response = response_map.map_exception(error)
    else:
        response = response_map.create_500(msg="Internal server error")

    return response


@app.after_request
def format_response(response):
    response.headers["Cache-Control"] = "no-cache"

    if response.status_code == 404:
        response = response_map.create_404()

    data = response.get_data()
    data += "\n"
    response.set_data(data)
    return response
