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
                "Authorization": "This better not be logged this way.",
                "SafeStuff": "This better be logged this way",
                "authorization": "not this",
                "auThOrIzAtion": "not this"
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
                "authorization: REDACTED\n"
                "auThOrIzAtion: REDACTED\n"
                "SafeStuff: This better be logged this way\n"
                "Authorization: REDACTED")
