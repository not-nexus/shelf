import pyproctor
from shelf.endpoint_decorators import decorators
from mock import Mock


class EndpointDecoratorsTest(pyproctor.TestBase):
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
            }
        })
        mock_container = type("FakeContainer", (), {
            "logger": logger_mock,
            "request": request_mock
        })

        @decorators.logheaders
        def test_log_headers(*args, **kwargs):
            pass

        test_log_headers(mock_container)
        logger_mock.info.assert_called_with("RESPONSE HEADERS : \n"
                "authentication: REDACTED\n"
                "accept: yes\n"
                "host: yes\n"
                "auThOrIzAtion: REDACTED\n"
                "Authorization: REDACTED\n"
                "authorization: REDACTED\n"
                "SafeStuff: This better be logged this way")

    def test_logbodies_errors_on_invalid_json(self):
        """
        """
        data = "{\"invalid\": ...}"
        valueErrorStr = "No JSON object could be decoded"
        logger_mock = Mock()
        logger_mock.info = Mock()
        logger_mock.exception = Mock()
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
        def test_log_bodies(*args, **kwargs):
            return request_mock

        test_log_bodies(mock_container)
        logger_mock.info.assert_any_call("Invalid JSON from request.")

        # Get the call arguments from logger_mock.exception,
        # and assert if the first argument is a ValueError with
        # the correct error message.
        args, kwargs = logger_mock.exception.call_args
        callArg = args[0]
        self.assertTrue(callArg.message == valueErrorStr)
        self.assertTrue(isinstance(callArg, ValueError))
