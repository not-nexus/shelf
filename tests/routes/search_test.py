from tests.functional_test_base import FunctionalTestBase


class SearchTest(FunctionalTestBase):
    def test_equality_case_sensitive_search(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/test; rel=child; title=test",
                ]
            }) \
            .post({
                "search": "artifactName=test"
            }, headers=self.auth)

    def test_wildcard_search(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/test; rel=child; title=test",
                    "/test/artifact/thing; rel=child; title=thing",
                ]
            }) \
            .post({
                "search": "artifactName=t*"
            }, headers=self.auth)

    def test_wildcard_first_search(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/test/Test; rel=child; title=test/Test",
                    "/test/artifact/test; rel=child; title=test",
                ]
            }) \
            .post({
                "search": "artifactName=*est"
            }, headers=self.auth)

    def test_version_search(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="test") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/a; rel=child; title=a",
                    "/test/artifact/blah; rel=child; title=blah",
                    "/test/artifact/this/that/other; rel=child; title=this/that/other",
                    "/test/artifact/thing; rel=child; title=thing",
                    "/test/artifact/zzzz; rel=child; title=zzzz"
                ]
            }) \
            .post({
                "search": "version~=1.1"
            }, headers=self.auth)

    def test_version_search_and_sort(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="test") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/thing; rel=child; title=thing",
                    "/test/artifact/a; rel=child; title=a",
                    "/test/artifact/blah; rel=child; title=blah",
                    "/test/artifact/zzzz; rel=child; title=zzzz"
                ]
            }) \
            .post({
                "search": "version~=1.2",
                "sort": "version, VERSION"
            }, headers=self.auth)

    def test_version_search_and_multi_sort(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="test") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/this/that/other; rel=child; title=this/that/other",
                    "/test/artifact/thing; rel=child; title=thing",
                    "/test/artifact/a; rel=child; title=a",
                    "/test/artifact/blah; rel=child; title=blah",
                    "/test/artifact/zzzz; rel=child; title=zzzz"
                ]
            }) \
            .post({
                "search": "version~=1.1",
                "sort": [
                    "version, VERSION",
                    # Testing the defaulting of SortType to ASC
                    "artifactName"
                ]
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
