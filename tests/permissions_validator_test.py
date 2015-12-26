import pyproctor
from pyshelf.permissions_validator import PermissionsValidator
import mock
import test_utils as utils


class PermissionsUnitTest(pyproctor.TestBase):
    def mock_dependencies(self, permissions, path, method, headers):
        request = mock.Mock()
        request.path = path
        request.method = method
        request.headers = headers
        container = mock.Mock()
        container.request = request
        storage = mock.Mock()
        storage.get_artifact_as_string = mock.MagicMock(return_value=permissions)
        storage.__exit__ = mock.MagicMock(return_value=False)
        storage.__enter__ = mock.MagicMock(return_value=storage)
        container.create_master_bucket_storage = mock.MagicMock(return_value=storage)
        self.validator = PermissionsValidator(container)
    
    def test_allowed_upload_with_full_access(self):
        self.mock_dependencies(utils.get_permissions_all(), "/artifact/upload-test", "POST", utils.auth_header())
        self.assertTrue(self.validator.allowed())

    def test_allowed_upload_with_readonly(self):
        self.mock_dependencies(utils.get_permissions_readonly(), "/artifact/upload-test", "POST", utils.auth_header())
        self.assertFalse(self.validator.allowed())

    def test_allowed_with_bad_key(self):
        self.mock_dependencies(utils.get_permissions_all(), "/artifact/upload-test", "POST", utils.auth_header(False))
        self.assertFalse(self.validator.allowed())

    def test_allowed_read_with_full_access(self):
        self.mock_dependencies(utils.get_permissions_all(), "/artifact/dir/dir2/dir3/nest-test", "GET", utils.auth_header())
        self.assertTrue(self.validator.allowed())

    def test_allowed_read_no_access(self):
        self.mock_dependencies(utils.get_permissions_func_test(), "/artifact/dir/test", "GET", utils.auth_header())
        self.assertFalse(self.validator.allowed())
