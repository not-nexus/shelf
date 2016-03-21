import flask
from pyshelf.routes.artifact import artifact
import pyshelf.response_map as response_map
import logging

app = flask.Flask(__name__)
app.register_blueprint(artifact)


@app.errorhandler(Exception)
def generic_exception_handler(error):
    """
        Prevents Exceptions flying all around the place.
    """
    app.logger.exception(error)
    return response_map.create_500(msg="Internal server error")


@app.after_request
def format_response(response):
    if response.status_code == 404:
        response = response_map.create_404()

    data = response.get_data()
    data += "\n"
    response.set_data(data)
    return response
