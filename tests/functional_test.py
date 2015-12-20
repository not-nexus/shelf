from tests.cloud_stubs import CloudFactoryStub
import pyproctor
import pyshelf.configure as configure


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
        artifact = self.test_client.get("/artifact/test", headers={"Authorization": "supersecuretoken"})
        data = artifact.get_data()

        if body:
            data = data.strip()
            self.assertEqual(body, data)

        self.assertEqual(
            status_code,
            artifact.status_code,
            "Expected status code %s did not match %s.  Body: %s" %
            (
                status_code,
                artifact.status_code,
                data
            )
        )

    def test_artifact_get_path(self):
        self.get_artifact_path("test", 200, "hello world")
