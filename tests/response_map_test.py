from pyshelf import response_map
import pyproctor
import json


class ResponseMapTest(pyproctor.TestBase):
    def test_map_exception_generic(self):
        expected_response = {
            "code": "internal_server_error",
            "message": "Internal server error"
        }
        response = response_map.map_exception(Exception("Just some error"))
        self.assertEquals(expected_response, json.loads(response.data))
        self.assertEquals(500, response.status_code)
