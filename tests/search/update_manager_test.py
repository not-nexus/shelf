from tests.unit_test_base import UnitTestBase
import tests.metadata_utils as utils
from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.container import Container as SearchContainer
from mock import Mock


class UpdateManagerTest(UnitTestBase):
    def setUp(self):
        config = {
            "elasticSearchHost": ["localhost:9200"],
            "test": {
                "accessKey": "test",
                "secretKey": "test",
            }
        }
        logger = Mock()
        self.search_container = SearchContainer(logger, config)
        self.update_manager = UpdateManager(self.search_container)
        self.update_manager.init("metadata")

    def tearDown(self):
        pass

    def test_metadata_document(self):
        self.update_manager.update("test_key", utils.get_meta())
        metadata = self.update_manager.get_metadata("test_key")
        expect = Metadata(meta={id: "test_,key"})
        expect.update(utils.get_meta())
        self.assertEqual(metadata, expect)
