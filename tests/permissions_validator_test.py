from unit_test_base import UnitTestBase
from pyshelf.permissions_validator import PermissionsValidator
from pyshelf.cloud.cloud_exceptions import ArtifactNotFoundError
from mock import MagicMock
import permission_utils as utils


class PermissionsUnitTest(UnitTestBase):
    def mock_dependencies(self, permissions, path, method, headers):
        self.container.request.path = path
        self.container.request.method = method
        self.container.request.headers = headers
        self.storage.get_artifact_as_string = MagicMock()

        def get_artifact(key):
            if key == "_keys/" + utils.VALID_KEY:
                return permissions
            return None

        self.storage.get_artifact_as_string.side_effect = get_artifact
        self.validator = PermissionsValidator(self.container)

    def test_allowed_upload_with_full_access(self):
        self.mock_dependencies(utils.get_permissions_all(), "/test/artifact/upload-test", "POST", utils.auth_header())
        self.assertTrue(self.validator.allowed())

    def test_allowed_upload_with_readonly(self):
        self.mock_dependencies(utils.get_permissions_readonly(), "/test/artifact/upload-test", "POST", utils.auth_header())
        self.assertFalse(self.validator.allowed())

    def test_allowed_with_bad_key(self):
        self.mock_dependencies(utils.get_permissions_all(), "/test/artifact/upload-test", "POST", utils.auth_header(False))
        self.assertFalse(self.validator.allowed())

    def test_allowed_read_with_full_access(self):
        self.mock_dependencies(
            utils.get_permissions_all(), "/test/artifact/dir/dir2/dir3/nest-test", "GET", utils.auth_header())
        self.assertTrue(self.validator.allowed())

    def test_allowed_read_no_access(self):
        self.mock_dependencies(utils.get_permissions_func_test(), "/test/artifact/dir/test", "GET", utils.auth_header())
        self.assertFalse(self.validator.allowed())

    def test_invalid_key(self):
        """ This is testing fake Authorization header issues """
        self.container.request.path = "/blah"
        self.container.request.method = "GET"
        self.container.request.headers = {"Authorization": "DOES NOT EXIST"}
        self.storage.get_artifact_as_string = MagicMock()
        self.storage.get_artifact_as_string.side_effect = ArtifactNotFoundError("DOES NOT EXIST")
        permissions = PermissionsValidator(self.container)
        self.assertFalse(permissions.allowed())
