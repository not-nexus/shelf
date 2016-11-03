import pyproctor
from shelf.app import generic_exception_handler
import json


class AppTest(pyproctor.TestBase):
    def test_generic_error_handler_non_cloud_exception(self):
        error = Exception("Ohhh just some catastrophic error")
        response = generic_exception_handler(error)
        expected = json.dumps({
            "code": "internal_server_error",
            "message": "Internal server error"
        })
        self.assertEqual(expected, response.data)
        self.assertEqual(500, response.status_code)
