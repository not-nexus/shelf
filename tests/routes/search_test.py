from tests.functional_test_base import FunctionalTestBase


class SearchTest(FunctionalTestBase):
    def test_search(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="test") \
            .expect(204, headers={
                "Links": []
            }) \
            .post({
                "search": "version~=1",
                "sort": "ASC, artifactName"
            }, headers=self.auth)
