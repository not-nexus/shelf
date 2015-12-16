import flask
from pyshelf.routes.artifact import artifact

app = flask.Flask(__name__)
app.register_blueprint(artifact, url_prefix="/artifact")

@app.after_request
def format_response(response):
    data = response.get_data()
    if response.status_code == 404:
        # TODO : Map a json response
        pass

    data += "\n"
    response.set_data(data)
    return response


@app.route("/r")
def get_routes():
    """
        Debug route for finding out which routes are available.
    """
    route_list = []
    for key, rule_list in app.url_map._rules_by_endpoint.iteritems():
        rule = rule_list[0]
        methods = "(" + ", ".join(rule.methods) + ")"
        route_list.append(rule.rule + " " + methods)

    route_list.sort()

    return "\n".join(route_list)
