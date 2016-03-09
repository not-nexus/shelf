from StringIO import StringIO
from functional_test_base import FunctionalTestBase
from pyshelf import configure


class ArtifactTest(FunctionalTestBase):
    def test_artifact_get_path(self):
        link = "/artifact/test; rel=self; title=test, /artifact/test/_meta; rel=metadata; title=metadata"
        self.route_tester \
            .artifact() \
            .route_params(path="test") \
            .expect(200, "hello world\n", headers={"Link": link}) \
            .get(headers=self.auth)

    def test_artifact_get_none(self):
        self.route_tester \
            .artifact() \
            .route_params(path="nada") \
            .expect(404, self.RESPONSE_404) \
            .get(headers=self.auth)

    def test_artifact_get_artifact_list(self):
        self.route_tester \
            .artifact() \
            .route_params(path="dir/dir2/dir3/dir4/") \
            .expect(204, headers={"Link": "/artifact/dir/dir2/dir3/dir4/test5; rel=child; title=dir/dir2/dir3/dir4/test5"}) \
            .get(headers=self.auth)

    def test_artifact_get_artifact_list_all(self):
        self.route_tester \
            .artifact() \
            .route_params(path="") \
            .expect(204, headers={
                "Link": "/artifact/test; rel=child; title=test, /artifact/dir/; rel=child; title=dir/"
            })\
            .get(headers=self.auth)

    def test_artifact_upload(self):
        self.route_tester.artifact().route_params(path="test-2")\
            .expect(201, {"success": True})\
            .post(data={"file": (StringIO("file contents"), "test.txt")}, headers=self.auth)

    def test_artifact_upload_no_permissions(self):
        self.route_tester.artifact().route_params(path="dir/test")\
            .expect(401, "Permission Denied\n")\
            .post(data={"file": (StringIO("file contents"), "test.txt")}, headers=self.auth)

    def test_artifact_upload_existing_artifact(self):
        self.route_tester.artifact().route_params(path="test")\
            .expect(403,
                {
                    "message": "Artifact by name test already exists in current directory",
                    "code": "duplicate_artifact"
                })\
            .post(data={"file": (StringIO("file contents"), "test.txt")}, headers=self.auth)

    def test_illegal_artifact_upload(self):
        self.route_tester \
            .artifact() \
            .route_params(path="_test")\
            .expect(403,
                {
                    "message": "The artifact name provided is not allowable. Please remove leading underscores.",
                    "code": "invalid_artifact_name"
                })\
            .post(data={"file": (StringIO("file contents"), "test.txt")}, headers=self.auth)
