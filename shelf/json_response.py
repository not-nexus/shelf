import flask
import json


class JsonResponse(flask.Response):
    def __init__(self, *args, **kwargs):
        super(JsonResponse, self).__init__(*args, **kwargs)
        self.headers["Content-Type"] = "application/json"

    def set_data(self, data):
        if not isinstance(data, basestring):
            data = json.dumps(data)

        super(JsonResponse, self).set_data(data)
