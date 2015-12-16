import flask

artifact = flask.Blueprint("artifact", __name__)

@artifact.route("/", methods=["GET"], defaults={"path": ""})
@artifact.route("/<path:path>", methods=["GET"])
def get_path(path):
    # TODO : This should list artifact resource links if it is a directory
    # or get the content of the artifact.
    return flask.Response("Path was " + path)
    
