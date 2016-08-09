from tests.functional_test_base import FunctionalTestBase
import tests.metadata_utils as meta_utils
from pyshelf.error_code import ErrorCode


class MetadataTest(FunctionalTestBase):
    def test_head_metadata(self):
        self.route_tester \
            .metadata() \
            .route_params(bucket_name="test", path="test") \
            .expect(200, headers={
                "Link": [
                    "</test/artifact/test>; rel=\"related\"; title=\"artifact\"",
                    "</test/artifact/test/_meta>; rel=\"self\"; title=\"metadata\""
                ]
            }) \
            .head(headers=self.auth)

    def test_get_metadata(self):
        self.route_tester \
            .metadata() \
            .route_params(bucket_name="test", path="test") \
            .expect(200, meta_utils.get_meta()) \
            .get(headers=self.auth)

    def test_put_metadata(self):
        self.route_tester \
            .metadata() \
            .route_params(bucket_name="test", path="dir/dir2/dir3/nest-test") \
            .expect(200, meta_utils.get_meta(name="nest-test", path="/test/artifact/dir/dir2/dir3/nest-test")) \
            .put(data=meta_utils.send_meta(), headers=self.auth)
        self.assert_metadata_matches("/test/artifact/dir/dir2/dir3/nest-test/_meta")

    def test_put_metadata_invalid_request_data(self):
        self.route_tester \
            .metadata() \
            .route_params(bucket_name="test", path="dir/dir2/dir3/nest-test") \
            .expect(400, {
                "code": "invalid_request_data_format",
                "message": "{u'notValue': u'biluga'} is not of additionalProperties False"
            }) \
            .put(data={"something": {"notValue": "biluga"}}, headers=self.auth)

    def test_put_metadata_invalid_json(self):
        self.route_tester \
            .metadata() \
            .route_params(bucket_name="test", path="dir/dir2/dir3/nest-test") \
            .expect(400, self.RESPONSE_INVALID_FORMAT) \
            .put(data='{"lol": ...}', headers=self.auth)

    def test_empty_metadata(self):
        """
            This will ensure that things are initialized
            correctly.

            See pyshelf.metadata.initializer.Initializer

            For the "empty" artifact see
            tests.functional_test_base.FunctionalTestBase.setup_artifacts
        """
        self.route_tester \
            .metadata() \
            .route_params(bucket_name="test", path="empty") \
            .expect(200, meta_utils.get_meta(name="empty", path="/test/artifact/empty")) \
            .put(data=meta_utils.send_meta(), headers=self.auth)

    def test_put_metadata_immutable(self):
        self.route_tester \
            .metadata() \
            .route_params(bucket_name="test", path="test") \
            .expect(200, meta_utils.get_meta()) \
            .put(data=meta_utils.send_meta_changed(), headers=self.auth)
        self.assert_metadata_matches("/test/artifact/test/_meta")

    def test_get_metadata_item(self):
        self.route_tester.metadata_item() \
            .route_params(bucket_name="test", path="test", item="tag") \
            .expect(200, meta_utils.get_meta()["tag"]) \
            .get(headers=self.auth)

    def test_get_hash(self):
        self.route_tester.metadata_item() \
            .route_params(bucket_name="test", path="test", item="md5Hash") \
            .expect(200, meta_utils.get_meta()["md5Hash"]) \
            .get(headers=self.auth)

    def test_post_metadata_item(self):
        self.route_tester \
            .metadata_item() \
            .route_params(bucket_name="test", path="test", item="tag2") \
            .expect(201, {"immutable": False, "name": "tag2", "value": "test"}) \
            .post(data=meta_utils.get_meta_item(), headers=self.auth)
        self.assert_metadata_matches("/test/artifact/test/_meta")

    def test_post_existing_metadata_item(self):
        self.route_tester \
            .metadata_item() \
            .route_params(bucket_name="test", path="test", item="tag1") \
            .expect(403, {"code": ErrorCode.FORBIDDEN, "message": "This metadata already exists."}) \
            .post(data=meta_utils.get_meta_item(), headers=self.auth)
        self.assert_metadata_matches("/test/artifact/test/_meta")

    def test_put_metadata_item(self):
        self.route_tester \
            .metadata_item() \
            .route_params(bucket_name="test", path="test", item="tag2") \
            .expect(201, {"immutable": False, "name": "tag2", "value": "test"}) \
            .put(data=meta_utils.get_meta_item(), headers=self.auth)
        self.assert_metadata_matches("/test/artifact/test/_meta")

    def test_put_metadata_existing_item(self):
        self.route_tester \
            .metadata_item() \
            .route_params(bucket_name="test", path="test", item="tag") \
            .expect(200, meta_utils.get_meta()["tag"]) \
            .put(data=meta_utils.get_meta()["tag"], headers=self.auth)
        self.assert_metadata_matches("/test/artifact/test/_meta")

    def test_put_metadata_item_poor_format(self):
        self.route_tester \
            .metadata_item() \
            .route_params(bucket_name="test", path="test", item="tag") \
            .expect(400, {
                "code": "invalid_request_data_format",
                "message": "[u'value', u'name'] is not of type object"
            }) \
            .put(data=["value", "name"], headers=self.auth)

    def test_delete_metadata_item(self):
        self.route_tester.metadata_item() \
            .route_params(bucket_name="test", path="test", item="tag") \
            .expect(204) \
            .delete(headers=self.auth)
        self.assert_metadata_matches("/test/artifact/test/_meta")

    def test_404_metadata_item(self):
        self.route_tester.metadata_item() \
            .route_params(bucket_name="test", path="test", item="ticktacktoe") \
            .expect(404, self.RESPONSE_404) \
            .get(headers=self.auth)

    def test_delete_metadata_immutable(self):
        self.route_tester.metadata_item() \
            .route_params(bucket_name="test", path="test", item="tag1") \
            .expect(403,
                    {
                        "code": "forbidden",
                        "message": "Cannot update immutable metadata."
                    }) \
            .delete(headers=self.auth)
        self.test_get_metadata_item()
        self.assert_metadata_matches("/test/artifact/test/_meta")
