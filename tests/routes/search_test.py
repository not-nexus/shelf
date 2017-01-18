from tests.functional_test_base import FunctionalTestBase


class SearchTest(FunctionalTestBase):
    def test_equality_case_sensitive_search(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "</test/artifact/test>; rel=\"item\"; title=\"artifact\"",
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
                    "</test/artifact/thing>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/test>; rel=\"item\"; title=\"artifact\""
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
                    "</test/artifact/dir/dir2/Test>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/test>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/dir/dir2/dir3/nest-test>; rel=\"item\"; title=\"artifact\""
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
                    "</test/artifact/blah>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/a>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/zzzz>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/this/that/other>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/thing>; rel=\"item\"; title=\"artifact\"",
                ]
            }) \
            .post({
                "search": "version~=1.1"
            }, headers=self.auth)

    def test_empty_search(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "</test/artifact/blah>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/a>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/zzzz>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/dir/dir2/Test>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/this/that/other>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/thing>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/test>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/dir/dir2/dir3/nest-test>; rel=\"item\"; title=\"artifact\""
                ]
            }) \
            .post(headers=self.auth)

    def test_empty_search_path(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="/dir/dir2/dir3") \
            .expect(204, headers={
                "Link": [
                    "</test/artifact/dir/dir2/dir3/nest-test>; rel=\"item\"; title=\"artifact\""
                ]
            }) \
            .post({}, headers=self.auth)

    def test_sort_metadata_property_does_not_exist(self):
        # Ensuring we don't blow up on a sort like this.
        # This was a bug cataloged https://github.com/kyle-long/shelf/issues/61
        # and changelog release v6.1
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "</test/artifact/blah>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/a>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/zzzz>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/dir/dir2/Test>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/this/that/other>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/thing>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/test>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/dir/dir2/dir3/nest-test>; rel=\"item\"; title=\"artifact\""
                ]
            }) \
            .post({"sort": "THINGS"}, headers=self.auth)

    def test_just_sort(self):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="/dir/dir2") \
            .expect(204, headers={
                "Link": [
                    "</test/artifact/dir/dir2/dir3/nest-test>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/dir/dir2/Test>; rel=\"item\"; title=\"artifact\""
                ]
            }) \
            .post({"sort": "version, VER"}, headers=self.auth)

    def test_version_search_and_sort(self):
        # Starts with lower version 1.2 and ends with 1.19.
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(204, headers={
                "Link": [
                    "</test/artifact/this/that/other>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/thing>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/blah>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/a>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/zzzz>; rel=\"item\"; title=\"artifact\""
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
                    "</test/artifact/this/that/other>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/thing>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/a>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/blah>; rel=\"item\"; title=\"artifact\"",
                    "</test/artifact/zzzz>; rel=\"item\"; title=\"artifact\""
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
                    "</test/artifact/dir/dir2/Test>; rel=\"item\"; title=\"artifact\""
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

    def search_with_bad_criteria(self, data, msg):
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path="") \
            .expect(400, {
                "code": "invalid_search_criteria",
                "message": msg
            }) \
            .post(data, headers=self.auth)

    def test_search_bad_search_criteria(self):
        msg = "u'imCool' is not of type u'array', u'imCool' does not match u'(?<!\\\\\\\\)='"
        self.search_with_bad_criteria({"search": "imCool"}, msg)

    def test_search_escaped_equal_criteria(self):
        msg = "u'imCool\\\\=notCoolDude' is not of type u'array', "
        msg += "u'imCool\\\\=notCoolDude' does not match u'(?<!\\\\\\\\)='"
        self.search_with_bad_criteria({"search": "imCool\=notCoolDude"}, msg)

    # Testing to make sure issue #63 is fixed.
    # (https://github.com/not-nexus/shelf/issues/63)
    def test_path_search_doesnt_match_artifact(self):
        self.run_path_search_on_directory("/test")

    def test_path_search_doesnt_match_artifact_trailing_slash(self):
        self.run_path_search_on_directory("/test/")

    def run_path_search_on_directory(self, path):
        self.add_metadata("/test/artifact/test/alsoATest")
        self.add_metadata("/test/artifact/test_lol")
        self.search_wrapper.refresh_index()
        self.route_tester \
            .search() \
            .route_params(bucket_name="test", path=path) \
            .expect(204,
                    headers={
                        "Link": [
                            "</test/artifact/test/alsoATest>; rel=\"item\"; title=\"artifact\""
                        ]
                    }) \
            .post(
                headers=self.auth
            )
