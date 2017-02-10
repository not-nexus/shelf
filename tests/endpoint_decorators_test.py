import pyproctor
from shelf.endpoint_decorators import decorators
from mock import Mock, call


class EndpointDecoratorsTest(pyproctor.TestBase):
    def setUp(self):
        self.response_mock = type("FakeResponse", (), {
            "data": {},
            "headers": {
                "content-type": "application/json"
            },
            "status_code": 200
        })

    def test_authorization_header_is_not_logged(self):
        """
            Very simple test. We found out the Authorization header was being
            logged by endpoint decorators. The only function that logs headers
            is decorators.logheaders, so this is testing that function. It
            must redact any headers added to the REDACTED_HEADERS list.
        """
        logger_mock = Mock()
        logger_mock.info = Mock()
        request_mock = type("FakeRequest", (), {
            "headers": {
                "Authorization": "no",
                "SafeStuff": "This better be logged this way",
                "authorization": "no",
                "auThOrIzAtion": "no",
                "authentication": "no",
                "host": "yes",
                "accept": "yes"
            },
            "method": "POST"
        })
        mock_container = type("FakeContainer", (), {
            "logger": logger_mock,
            "request": request_mock
        })

        @decorators.logheaders
        def test_log_headers(*args, **kwargs):
            return self.response_mock

        test_log_headers(mock_container)
        logger_mock.info.assert_has_calls(
            [
                call(
                    "REQUEST HEADERS : \n"
                    "authentication: REDACTED\n"
                    "accept: yes\n"
                    "host: yes\n"
                    "auThOrIzAtion: REDACTED\n"
                    "Authorization: REDACTED\n"
                    "authorization: REDACTED\n"
                    "SafeStuff: This better be logged this way"
                ),
                call("RESPONSE HEADERS : \nSTATUS CODE: 200\ncontent-type: application/json")
            ]
        )

    def test_logbodies_errors_on_invalid_json(self):
        """
            Tests the logbodies function to make sure it correctly
            catches invalid JSON requests.
        """
        data = "{\"invalid\": ...}"
        valueErrorStr = "No JSON object could be decoded"
        logger_mock = Mock()
        request_mock = type("FakeRequest", (), {
            "headers": {
                "content-type": "application/json"
            },
            "data": data
        })
        request_mock.get_data = Mock(return_value=data)
        mock_container = type("FakeContainer", (), {
            "logger": logger_mock,
            "request": request_mock
        })

        @decorators.logbodies
        def test_log_bodies(container):
            return self.response_mock

        test_log_bodies(mock_container)
        logger_mock.info.assert_any_call("Invalid JSON from request.")

        # Get the call arguments from logger_mock.exception,
        # and assert if the first argument is a ValueError with
        # the correct error message.
        callArg = logger_mock.exception.call_args[0][0]
        self.assertEqual(ValueError, type(callArg))
        self.assertEqual(valueErrorStr, callArg.message)
