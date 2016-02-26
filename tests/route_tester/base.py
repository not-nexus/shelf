import json


class Base(object):
    def __init__(self, test, test_client):
        self.test_client = test_client
        self.test = test
        self._endpoint = None
        self.params = None
        self.status_code = None
        self.response = None
        self.headers = None
        self.route = None

    @property
    def endpoint(self):
        if not self._endpoint:
            self._endpoint = self.route.format(**self.params)
        return self._endpoint

    def route_params(self, **params):
        """
            Sets the route parameters

            Arg:
                params(dict): Names and values of route parameters.

            Returns:
                self(route_tester.base.Base)
        """
        self.params = params
        return self

    def expect(self, status_code, response=None, headers=None):
        """
            Sets the expected status_code and response. To be asserted.

            Arg:
                status_code(int): status code of response expected.
                response(object): expected decoded response.

            Returns:
                self(route_test.base.Base)
        """
        self.status_code = status_code
        self.response = response
        self.headers = headers
        return self

    def get(self, data=None, headers=None):
        """
            Performs a GET request on the test client and asserts the response.

            Arg:
                data(None or dict): data for GET request.
        """
        data = self._encode(data)
        response = self.test_client.get(self.endpoint, data=data, headers=headers)
        self._assert(response)

    def post(self, data, headers=None):
        """
            Performs a POST request on the test client and asserts the response.

            Arg:
                data(dict): data for POST request.
        """
        data = self._encode(data)
        response = self.test_client.post(self.endpoint, data=data, headers=headers)
        self._assert(response)

    def put(self, data, headers=None):
        """
            Performs a PUT request on the test client and asserts the response.

            Arg:
                data(dict): data for PUT request.
        """
        data = self._encode(data)
        response = self.test_client.put(self.endpoint, data=data, headers=headers)
        self._assert(response)

    def delete(self, data=None, headers=None):
        """
            Performs a DELETE request on the test client and asserts the response.

            Arg:
                data(None or dict): data for DELETE request.
        """
        data = self._encode(data)
        response = self.test_client.delete(self.endpoint, data=data, headers=headers)
        self._assert(response)

    def _assert(self, actual_response):
        if self.status_code:
            self.test.assertEqual(self.status_code, actual_response.status_code)
        if self.response:
            data = actual_response.get_data()
            try:
                actual = json.loads(data)
            except ValueError:
                pass
                actual = data

            self.test.assertEqual(self.response, actual)
        if self.headers:
            for key, value in self.headers.iteritems():
                self.test.assertEqual(value, actual_response.headers.get(key))

    def _encode(self, data):
        if data is not None:
            try:
                data = json.dumps(data)
            except TypeError:
                pass
        return data
