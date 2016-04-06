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
                    "/test/artifact/thing; rel=child; title=thing",
                    "/test/artifact/test; rel=child; title=test"
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
                    "/test/artifact/dir/dir2/Test; rel=child; title=dir/dir2/Test",
                    "/test/artifact/test; rel=child; title=test",
                    "/test/artifact/dir/dir2/dir3/nest-test; rel=child; title=dir/dir2/dir3/nest-test"
                ]
            }) \
            .post({
                "search": "artifactName=*est"
            }, headers=self.auth)

    def test_version_search(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/blah; rel=child; title=blah",
                    "/test/artifact/a; rel=child; title=a",
                    "/test/artifact/zzzz; rel=child; title=zzzz",
                    "/test/artifact/this/that/other; rel=child; title=this/that/other",
                    "/test/artifact/thing; rel=child; title=thing",
                ]
            }) \
            .post({
                "search": "version~=1.1"
            }, headers=self.auth)

    def test_version_search_and_sort(self):
        # Starts with lower version 1.2 and ends with 1.19.
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/this/that/other; rel=child; title=this/that/other",
                    "/test/artifact/thing; rel=child; title=thing",
                    "/test/artifact/blah; rel=child; title=blah",
                    "/test/artifact/a; rel=child; title=a",
                    "/test/artifact/zzzz; rel=child; title=zzzz"
                ]
            }) \
            .post({
                "search": "version~=1.2",
                "sort": "version, VER, ASC"
            }, headers=self.auth)

    def test_version_search_and_multi_sort(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
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

    def test_search_with_path(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="dir/dir2") \
            .expect(204, headers={
                "Link": [
                    "/test/artifact/dir/dir2/Test; rel=child; title=dir/dir2/Test"
                ]
            }) \
            .post({
                "search": "artifactName=Test"
            }, headers=self.auth)

    def test_search_no_results(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": []
            }) \
            .post({
                "search": "artifactName=baloba"
            }, headers=self.auth)

    def search_with_bad_criteria(self, data):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(400, {
                "code": "bad_request",
                "message": "Invalid search and/or sort criteria."
            }) \
            .post(data, headers=self.auth)

    def test_search_bad_search_criteria(self):
        self.search_with_bad_criteria({"search": "imCool"})

    def test_search_escaped_equal_criteria(self):
        self.search_with_bad_criteria({"search": "imCool\=notCoolDude"})
