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


class FunctionalTest(pyproctor.TestBase):
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
        #Metadata for artifacts
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

    def get_artifact_path(self, path, status_code=200, body=None):
        artifact = self.test_client.get(path, headers=self.auth)
        self.assert_response(status_code, artifact, body)

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

    def upload_artifact(self, path, status_code=201, body=None):
        response = self.test_client.post(
            path,
            data={'file': (StringIO('file contents'), 'test.txt')},
            headers=self.auth)

        self.assert_response(status_code, response, body)

    def get_artifact_metadata(self, path, status_code=200, body=None):
        response = self.test_client.get(path, headers=self.auth)
        self.assert_response(status_code, response, body)

    def set_artifact_metadata(self, path, status_code=201, body=None, data=meta_utils.send_meta()):
        response = self.test_client.put(path, data=data, headers=self.auth)
        self.assert_response(status_code, response, body)

    def get_artifact_metadata_item(self, path, status_code=200, body=None):
        response = self.test_client.get(path, headers=self.auth)
        self.assert_response(status_code, response, body)

    def update_metadata_item_post(self, path, status_code, body=None):
        response = self.test_client.post(path, data=meta_utils.send_meta_item(), headers=self.auth)
        self.assert_response(status_code, response, body)

    def update_metadata_item_put(self, path, status_code, body=None):
        response = self.test_client.put(path, data=meta_utils.send_meta_item(), headers=self.auth)
        self.assert_response(status_code, response, body)

    def delete_meta_item(self, path, status_code=200, body=None):
        response = self.test_client.delete(path, headers=self.auth)
        self.assert_response(status_code, response, body)

    def test_artifact_get_path(self):
        self.get_artifact_path("/artifact/test", 200, "hello world")

    def test_artifact_get_none(self):
        self.get_artifact_path(
            "/artifact/nothing",
            404,
            {
                "message": "Resource not found",
                "code": "resource_not_found"
            }
        )

    def test_artifact_upload(self):
        self.upload_artifact("/artifact/test-2", 201, {"success": True})

    def test_artifact_upload_permissions(self):
        self.upload_artifact("/artifact/dir/nest-test", 401, "Permission Denied")
        self.get_artifact_path("/artifact/dir/test", 401, "Permission Denied")

    def test_artifact_upload_existing_artifact(self):
        self.upload_artifact(
            "/artifact/test",
            403,
            {
                "message": "Artifact by name test already exists in current directory",
                "code": "duplicate_artifact"
            }
        )

    def test_illegal_artifact_upload(self):
        self.upload_artifact(
            "/artifact/_test",
            403,
            {
                "message": "The artifact name provided is not an allowable name. Please remove leading underscores.",
                "code": "invalid_artifact_name"
            }
        )

    def test_get_metadata(self):
        self.get_artifact_metadata(
            "/artifact/test/_meta",
            200,
            meta_utils.get_meta()
        )

    def test_set_metadata(self):
        self.set_artifact_metadata(
            "/artifact/dir/dir2/dir3/nest-test/_meta",
            201,
            {"success": True}
        )

    def test_set_metadata_immutable(self):
        self.set_artifact_metadata(
            "/artifact/test/_meta",
            201,
            {"success": True},
            meta_utils.send_meta_changed()
        )
        self.get_artifact_metadata(
            "/artifact/test/_meta",
            200,
            meta_utils.get_meta()
        )

    def test_get_metadata_item(self):
        self.get_artifact_metadata_item(
            "/artifact/test/_meta/tag",
            200,
            meta_utils.get_meta()["tag"]
        )
        #test get hash
        self.get_artifact_metadata(
            "/artifact/test/_meta/md5Hash",
            200,
            meta_utils.get_meta()["md5Hash"]
        )

    def test_post_metadata_item(self):
        self.update_metadata_item_post(
            "/artifact/test/_meta/tag2",
            201,
            {"success": True}
        )
        self.update_metadata_item_post(
            "/artifact/test/_meta/tag2",
            200,
            {"success": True}
        )

    def test_put_metadata_item(self):
        self.update_metadata_item_post(
            "/artifact/test/_meta/tag2",
            201,
            {"success": True}
        )
        self.update_metadata_item_put(
            "/artifact/test/_meta/tag2",
            200,
            {"success": True}
        )

    def test_delete_metadata_item(self):
        self.delete_meta_item(
            "/artifact/test/_meta/tag",
            200,
            {"success": True}
        )
        self.get_artifact_metadata_item(
            "/artifact/test/_meta/tag",
            404,
            {
                "message": "Resource not found",
                "code": "resource_not_found"
            }
        )

    def test_delete_metadata_immutable(self):
        self.delete_meta_item(
            "/artifact/test/_meta/tag1",
            200,
            {"success": True}
        )
        self.test_get_metadata_item()
