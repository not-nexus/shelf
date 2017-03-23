from tests.functional_test_base import FunctionalTestBase
from shelf.link_title import LinkTitle


class ListShelvesTest(FunctionalTestBase):
    def test_list_shelves_no_auth(self):
        self.route_tester \
            .base("/") \
            .expect(401) \
            .get()

    def test_list_shelves(self):
        expectedResponse = [
            "test",
            "b2"
        ]
        expectedHeaders = {
            "Link": [
                "</test/artifact/>; rel=\"collection\"; title=\"{0}\"".format(LinkTitle.ARTIFACT_ROOT),
                "</b2/artifact/>; rel=\"collection\"; title=\"{0}\"".format(LinkTitle.ARTIFACT_ROOT),
            ]
        }
        self.route_tester \
            .base("/") \
            .expect(200, response=expectedResponse, headers=expectedHeaders) \
            .get(headers=self.auth)
