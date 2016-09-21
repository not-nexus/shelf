import pyproctor
from pyshelf.permissions_validator import PermissionsValidator
from mock import Mock
import yaml


class PermissionsValidatorTest(pyproctor.TestBase):
    def setUp(self):
        self.permissions_no_name = {
            "token": "TOKEN",
            "write": ["/*"],
            "read": ["/*"]
        }

    def test_permissions_artifact_name(self):
        container_mock = Mock()
        storage_mock = Mock()
        storage_mock.__enter__ = Mock(return_value=storage_mock)
        storage_mock.__exit__ = Mock(return_value=False)
        storage_mock.get_artifact_as_string = Mock(return_value=yaml.dump(self.permissions_no_name))
        request_mock = Mock()
        request_mock.headers = {"Authorization": "TOKEN"}
        container_mock = type(
            "FakeContainer",
            (),
            {"request": request_mock, "create_silent_bucket_storage": Mock(return_value=storage_mock), "logger": Mock()}
        )
        validator = PermissionsValidator(container_mock())
        self.asserts.json_equals(self.permissions_no_name, validator.permissions)
        storage_mock.get_artifact_as_string.assert_called_with("_keys/TOKEN")
        container_mock.logger.warning.assert_called_with("Name was not set in authorization token.")
