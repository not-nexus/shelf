from tests.functional_test_base import FunctionalTestBase


class SearchTest(FunctionalTestBase):
    def test_wildcard_search(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/a; rel=child; title=a",
                    "/test/artifact/blah; rel=child; title=blah",
                    "/test/artifact/this/that/other; rel=child; title=this/that/other",
                    "/test/artifact/test; rel=child; title=test",
                    "/test/artifact/thing; rel=child; title=thing",
                    "/test/artifact/zzzz; rel=child; title=zzzz"
                ]
            }) \
            .post({
                "search": "artifactName=*"
            }, headers=self.auth)

    def test_search_no_results(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="test") \
            .expect(204, headers={
                "Link": []
            }) \
            .post({
                "search": "artifactName=baloba"
            }, headers=self.auth)

    def test_search_no_results(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="test") \
            .expect(204, headers={
                "Link": []
            }) \
            .post({
                "search": "artifactName=baloba"
            }, headers=self.auth)
