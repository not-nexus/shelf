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
        self.headers = None
        if headers:
            self.headers = self._normalize_headers(headers)
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
                actual = data

            if isinstance(actual, basestring):
                self.test.assertEqual(self.response, actual)
            else:
                self.test.asserts.json_equals(self.response, actual)
        if self.headers:
            self._assert_headers(actual_response.headers)

    def _assert_headers(self, actual_headers):
        """
            Validates that the expected headers match the actual headers.

            Args:
                actual_headers(werkzeug.datastructures.EnvironHeaders)

        """
        for key, expected_list in self.headers.iteritems():
            actual_list = actual_headers.getlist(key)
            self.test.assertEqual(expected_list, actual_list)

    def _encode(self, data):
        if data is not None:
            try:
                data = json.dumps(data)
            except TypeError:
                pass
        return data

    def _normalize_headers(self, headers):
        """
            Forces all values to be a list if it is
            not already a list.  This is so that I have
            an expected format to assert against later.

            This change is supposed to fix the problem where
            we can have multiple of the same response header

            Args:
                headers(dict): Orginal headers

            Returns:
                dict<list>
        """
        new_headers = {}
        for key, value in headers.iteritems():
            if not isinstance(value, list):
                value = [value]

            new_headers[key] = value

        return new_headers
