from StringIO import StringIO
from tests.functional_test_base import FunctionalTestBase


class ArtifactTest(FunctionalTestBase):
    def test_artifact_get_path(self):
        link = [
            "/test/artifact/test; rel=self; title=artifact",
            "/test/artifact/test/_meta; rel=related; title=metadata"
        ]
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="test", path="test") \
            .expect(200, "hello world\n", headers={"Link": link}) \
            .get(headers=self.auth)

    def test_artifact_no_permissions(self):
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="test", path="dir/test") \
            .expect(401, "Permission Denied\n") \
            .get(headers=self.auth)

    def test_artifact_get_none(self):
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="test", path="nada") \
            .expect(404, self.RESPONSE_404) \
            .get(headers=self.auth)

    def test_no_permission_file(self):
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="test", path="billy-bob-thorton") \
            .expect(401, "Permission Denied\n") \
            .get(headers={"Authorization": "bkdjfaojdklfjakdjHELLOWORLDlajdfjkadjok"})

    def artifact_get_list(self, path):
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="test", path=path) \
            .expect(204, headers={
                "Link": "/test/artifact/dir/dir2/dir3/dir4/test5; rel=item; title=artifact"
            }) \
            .get(headers=self.auth)

    def test_artifact_get_artifact_list(self):
        self.artifact_get_list("dir/dir2/dir3/dir4/")

    def test_artifact_get_artifact_list_no_trailing_slash(self):
        self.artifact_get_list("dir/dir2/dir3/dir4")

    def test_artifact_get_artifact_list_all(self):
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/empty; rel=item; title=artifact",
                    "/test/artifact/test; rel=item; title=artifact",
                    "/test/artifact/dir/; rel=collection; title=a collection of artifacts",
                    "/test/artifact/this/; rel=collection; title=a collection of artifacts"
                ]
            }) \
            .get(headers=self.auth)

    def test_artifact_head_from_root(self):
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/empty; rel=item; title=artifact",
                    "/test/artifact/test; rel=item; title=artifact",
                    "/test/artifact/dir/; rel=collection; title=a collection of artifacts",
                    "/test/artifact/this/; rel=collection; title=a collection of artifacts"
                ]
            }) \
            .head(headers=self.auth)

    def test_artifact_upload(self):
        self.route_tester.artifact() \
            .route_params(bucket_name="test", path="test-2") \
            .expect(201, {"success": True}, headers={"Location": "http://localhost/test/artifact/test-2"}) \
            .post(data={"file": (StringIO("file contents"), "test.txt")}, headers=self.auth)

    def test_artifact_upload_other_bucket(self):
        self.route_tester.artifact() \
            .route_params(bucket_name="bucket2", path="nick-drake") \
            .expect(201, {"success": True}, headers={"Location": "http://localhost/bucket2/artifact/nick-drake"}) \
            .post(data={"file": (StringIO("file contents"), "nick-drake.txt")}, headers=self.auth)

    def test_artifact_upload_no_permissions(self):
        self.route_tester.artifact() \
            .route_params(bucket_name="test", path="dir/test") \
            .expect(401, "Permission Denied\n") \
            .post(data={"file": (StringIO("file contents"), "test.txt")}, headers=self.auth)

    def test_artifact_upload_existing_artifact(self):
        self.route_tester.artifact() \
            .route_params(bucket_name="test", path="test") \
            .expect(403, self.RESPONSE_DUPLICATE) \
            .post(data={"file": (StringIO("file contents"), "test.txt")}, headers=self.auth)

    def test_illegal_artifact_upload(self):
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="test", path="_test") \
            .expect(403, self.RESPONSE_INVALID_NAME) \
            .post(data={"file": (StringIO("file contents"), "test.txt")}, headers=self.auth)

    def test_bucket_configuration_doesnt_exist(self):
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="lol-this-doesnt-exist", path="hello/there") \
            .expect(404, self.RESPONSE_404) \
            .get(headers=self.auth)

    def test_bucket_doesnt_exist(self):
        self.route_tester \
            .artifact() \
            .route_params(bucket_name="thisBucketDoesntExistLol", path="hello/there") \
            .expect(500, self.response_500()) \
            .get(headers=self.auth)
