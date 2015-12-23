import pyproctor
import pyshelf.configure as configure
from StringIO import StringIO
from moto import mock_s3
import boto
from boto.s3.key import Key


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
        key = Key(self.test_bucket)
        key.key = "test"
        key.set_contents_from_string("hello world")
        self.create_auth_key()

    def create_auth_key(self):
        self.auth = {"Authorization": "190a64931e6e49ccb9917c7f32a29d19"}
        key_name = "_keys/{}".format(self.auth['Authorization'])
        auth_key = Key(self.test_bucket, key_name)
        auth_key.set_contents_from_string("""
                    name: 'Andy Gertjejansen'
                    token: '190a64931e6e49ccb9917c7f32a29d19'
                    write:
                      - 'andy_gertjejansen/**'
                      - 'kyle_long/andy_upload_access/*'
                    read:
                      - '/**'""")

    def tearDown(self):
        self.moto_s3.stop()

    def get_artifact_path(self, path, status_code=200, body=None):
        artifact = self.test_client.get(path, headers=self.auth)
        self.assert_response(status_code, artifact, body)

    def assert_response(self, status_code, response, body=None):
        data = response.get_data()

        if body:
            data = data.strip()
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

    def test_artifact_get_path(self):
        self.get_artifact_path("/artifact/test", 200, "hello world")

    def test_artifact_get_none(self):
        self.get_artifact_path("/artifact/nothing", 404)
    
    def test_artifact_upload(self):
        self.upload_artifact("/artifact/test-2", 201)

    def test_duplicate_artifact_upload(self):
        self.upload_artifact("/artifact/test", 403)

    def test_illegal_artifact_upload(self):
        self.upload_artifact("/artifact/_test", 403)
