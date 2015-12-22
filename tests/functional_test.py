from tests.cloud_stubs import CloudFactoryStub
import pyproctor
import pyshelf.configure as configure
import os
from StringIO import StringIO


class FunctionalTest(pyproctor.TestBase):
    def setUp(self):
        config = {
            "accessKey": "test",
            "secretKey": "test",
            "bucketName": "test"
        }
        import pyshelf.cloud.storage
        pyproctor.MonkeyPatcher.patch(pyshelf.cloud.factory, "Factory", CloudFactoryStub)
        from pyshelf.app import app
        self.app = app
        self.app.config.update(config)
        configure.logger(app.logger, "DEBUG")
        self.test_client = app.test_client()

    def tearDown(self):
        CloudFactoryStub.reset()

    def get_artifact_path(self, path, status_code=200, body=None):
        artifact = self.test_client.get(path, headers={"Authorization": "supersecuretoken"})
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
            headers={"Authorization": "supersecuretoken"})

        self.assert_response(status_code, response, body)

    def test_artifact_get_path(self):
        self.get_artifact_path("/artifact/test", 200, "hello world")

    def test_artifact_upload(self):
        self.upload_artifact("/artifact/test", 201)
