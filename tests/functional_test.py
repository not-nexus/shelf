from StringIO import StringIO
from boto.s3.key import Key
from moto import mock_s3
import boto
import json
import pyproctor
import pyshelf.configure as configure
import permission_utils as utils
import metadata_utils as meta_utils
import yaml
from tests.route_tester.tester import Tester


class FunctionalTest(pyproctor.TestBase):
    RESPONSE_404 = {
        "message": "Resource not found",
        "code": "resource_not_found"
    }

    def setUp(self):
        config = {
            "accessKey": "test",
            "secretKey": "test",
            "bucketName": "test"
        }
        self.configure_moto()
        from pyshelf.app import app
        self.app = app
        self.app.config.update(config)
        configure.logger(app.logger, "DEBUG")
        self.test_client = app.test_client()
        self._route_tester = None

    def configure_moto(self):
        self.moto_s3 = mock_s3()
        self.moto_s3.start()
        self.boto_connection = boto.connect_s3()
        self.boto_connection.create_bucket("test")
        self.test_bucket = self.boto_connection.get_bucket("test")
        self.configure_artifacts()
        self.create_auth_key()

    def configure_artifacts(self):
        key = Key(self.test_bucket, "test")
        key.set_contents_from_string("hello world")
        nested_key = Key(self.test_bucket, "/dir/dir2/dir3/nest-test")
        nested_key.set_contents_from_string("hello world")
        # Metadata for artifacts
        meta_key = Key(self.test_bucket, "_metadata_test.yaml")
        meta_key.set_contents_from_string(yaml.dump(meta_utils.get_meta()))
        nest_meta_key = Key(self.test_bucket, "/dir/dir2/dir3/_metadata_nest-test.yaml")
        nest_meta_key.set_contents_from_string("")

    def create_auth_key(self):
        self.auth = utils.auth_header()
        key_name = "_keys/{}".format(self.auth['Authorization'])
        auth_key = Key(self.test_bucket, key_name)
        auth_key.set_contents_from_string(utils.get_permissions_func_test())

    def tearDown(self):
        self.moto_s3.stop()

    @property
    def route_tester(self):
        if not self._route_tester:
            self._route_tester = Tester(self, self.test_client)

        return self._route_tester

    def assert_response(self, status_code, response, body=None):
        data = response.get_data()
        if body:
            data = data.strip()
            try:
                data = json.loads(data)
            except ValueError:
                # This is expected if it is just a string.
                pass

            self.assertEqual(body, data)

        self.assertEqual(
            status_code,
            response.status_code,
            "Expected status code %s did not match %s.  Body: %s" %
            (
                status_code,
                response.status_code,
                data
            )
        )

    def test_artifact_get_path(self):
        self.route_tester.artifact().route_params(path="test").expect(200, "hello world\n").get(headers=self.auth)

    def test_artifact_get_none(self):
        self.route_tester.artifact().route_params(path="nada").expect(404, self.RESPONSE_404).get(headers=self.auth)

    def test_artifact_upload(self):
        self.route_tester.artifact().route_params(path="test-2")\
            .expect(201, {"success": True})\
            .post(data={'file': (StringIO('file contents'), 'test.txt')}, headers=self.auth)

    def test_artifact_upload_no_permissions(self):
        self.route_tester.artifact().route_params(path="dir/test")\
            .expect(401, "Permission Denied\n")\
            .post(data={'file': (StringIO('file contents'), 'test.txt')}, headers=self.auth)

    def test_artifact_upload_existing_artifact(self):
        self.route_tester.artifact().route_params(path="test")\
            .expect(403,
                {
                    "message": "Artifact by name test already exists in current directory",
                    "code": "duplicate_artifact"
                })\
            .post(data={'file': (StringIO('file contents'), 'test.txt')}, headers=self.auth)

    def test_illegal_artifact_upload(self):
        self.route_tester.artifact().route_params(path="_test")\
            .expect(403,
                {
                    "message": "The artifact name provided is not an allowable name. Please remove leading underscores.",
                    "code": "invalid_artifact_name"
                })\
            .post(data={'file': (StringIO('file contents'), 'test.txt')}, headers=self.auth)

    def test_get_metadata(self):
        self.route_tester.metadata().route_params(path="test").expect(200, meta_utils.get_meta()).get(headers=self.auth)

    def test_put_metadata(self):
        self.route_tester.metadata().route_params(path="dir/dir2/dir3/nest-test")\
            .expect(201, {"success": True})\
            .put(data=meta_utils.send_meta(), headers=self.auth)

    def test_put_metadata_immutable(self):
        self.route_tester.metadata().route_params(path="test")\
            .expect(201, {"success": True})\
            .put(data=meta_utils.send_meta_changed(), headers=self.auth)

    def test_get_metadata_item(self):
        self.route_tester.metadata_item().route_params(path="test", item="tag")\
            .expect(200, meta_utils.get_meta()["tag"])\
            .get(headers=self.auth)

    def test_get_hash(self):
        self.route_tester.metadata_item().route_params(path="test", item="md5Hash")\
            .expect(200, meta_utils.get_meta()["md5Hash"])\
            .get(headers=self.auth)

    def test_post_metadata_item(self):
        self.route_tester.metadata_item().route_params(path="test", item="tag2")\
            .expect(201, {"success": True})\
            .post(data=meta_utils.get_meta_item(), headers=self.auth)

    def test_post_ignore_metadata_item(self):
        self.route_tester.metadata_item().route_params(path="test", item="tag2")\
            .expect(201, {"success": True})\
            .post(data=meta_utils.get_meta_item(), headers=self.auth)

    def test_put_metadata_item(self):
        self.route_tester.metadata_item().route_params(path="test", item="tag2")\
            .expect(201, {"success": True})\
            .put(data=meta_utils.get_meta_item(), headers=self.auth)

    def test_delete_metadata_item(self):
        self.route_tester.metadata_item().route_params(path="test", item="tag")\
            .expect(200, {"success": True})\
            .delete(headers=self.auth)

    def test_delete_metadata_immutable(self):
        self.route_tester.metadata_item().route_params(path="test", item="tag1")\
            .expect(200, {"success": True})\
            .delete(headers=self.auth)
        self.test_get_metadata_item()
