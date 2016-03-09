from functional_test_base import FunctionalTestBase
import metadata_utils as meta_utils


class MetadataTest(FunctionalTestBase):
    def test_get_metadata(self):
        self.route_tester \
            .metadata() \
            .route_params(path="test") \
            .expect(200, meta_utils.get_meta()) \
            .get(headers=self.auth)

    def test_put_metadata(self):
        self.route_tester \
            .metadata() \
            .route_params(path="dir/dir2/dir3/nest-test")\
            .expect(201, meta_utils.get_meta())\
            .put(data=meta_utils.send_meta(), headers=self.auth)

    def test_put_metadata_immutable(self):
        self.route_tester \
            .metadata() \
            .route_params(path="test") \
            .expect(201, meta_utils.get_meta()) \
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
        self.route_tester \
            .metadata_item() \
            .route_params(path="test", item="tag2") \
            .expect(201, {"immutable": False, "name": "tag2", "value": "test"}) \
            .post(data=meta_utils.get_meta_item(), headers=self.auth)

    def test_post_existing_metadata_item(self):
        self.route_tester \
            .metadata_item() \
            .route_params(path="test", item="tag1") \
            .expect(403,
                {
                    "code": "forbidden",
                    "message": "Forbidden"
                }) \
            .post(data=meta_utils.get_meta_item(), headers=self.auth)

    def test_put_metadata_item(self):
        self.route_tester \
            .metadata_item() \
            .route_params(path="test", item="tag2") \
            .expect(201, {"immutable": False, "name": "tag2", "value": "test"}) \
            .put(data=meta_utils.get_meta_item(), headers=self.auth)

    def test_put_metadata_existing_item(self):
        self.route_tester \
            .metadata_item() \
            .route_params(path="test", item="tag") \
            .expect(200, meta_utils.get_meta()["tag"]) \
            .put(data=meta_utils.get_meta()["tag"], headers=self.auth)

    def test_delete_metadata_item(self):
        self.route_tester.metadata_item().route_params(path="test", item="tag")\
            .expect(204)\
            .delete(headers=self.auth)

    def test_delete_metadata_immutable(self):
        self.route_tester.metadata_item().route_params(path="test", item="tag1")\
            .expect(403,
                    {
                        "code": "forbidden",
                        "message": "The metadata item tag1 is immutable."
                    })\
            .delete(headers=self.auth)
        self.test_get_metadata_item()
