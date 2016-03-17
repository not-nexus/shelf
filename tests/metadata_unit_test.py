from unit_test_base import UnitTestBase
from pyshelf.cloud.metadata_mapper import MetadataMapper
from pyshelf.cloud.cloud_exceptions import ImmutableMetadataError
import metadata_utils as utils
from mock import MagicMock, Mock
import yaml


class MetadataUnitTest(UnitTestBase):
    def _setup_metadata(self, artifact_name, metadata=None):
        exists = (metadata is not None)
        self.storage.artifact_exists = MagicMock(return_value=exists)

        def get_metadata():
            return yaml.dumps(metadata)

        self.storage.get_artifact_as_string = MagicMock()
        self.storage.get_artifact_as_string.side_effect = get_metadata
        self.storage.get_etag = MagicMock(return_value="md5HashIsForNoobs")

    def test_create_metadata(self):
        self._setup_metadata("test")
        meta_mapper = MetadataMapper(self.container, "test")
        meta = {
            "value": "this is most certainly new",
            "immutable": True
        }
        success = meta_mapper.create_metadata_item(meta, "metaItem")
        self.assertTrue(success)
        # Test that overwrite fails. Only creates does not update.
        success = meta_mapper.create_metadata_item(meta, "metaItem")
        self.assertFalse(success)

    def test_set_metadata(self):
        self._setup_metadata("non-existant")
        meta_mapper = MetadataMapper(self.container, "non-existant")
        meta = {
            "metaItem": {
                "value": "this is most certainly new",
                "immutable": False
            }
        }
        expected_meta = {
            "metaItem": {
                "value": "lolol",
                "immutable": True
            },
            "md5Hash": {
                "name": "md5Hash",
                "value": "md5HashIsForNoobs",
                "immutable": True
            },
            "artifactPath": {
                "name": "artifactPath",
                "value": "non-existant",
                "immutable": True
            },
            "artifactName": {
                "name": "artifactName",
                "value": "non-existant",
                "immutable": True
            }
        }
        meta_mapper.set_metadata(meta)
        item = meta_mapper.get_metadata("metaItem")
        self.assertEqual(item, {"value": "this is most certainly new", "immutable": False})
        meta_mapper.set_metadata({"value": "lolol", "immutable": True}, "metaItem")
        act_meta = meta_mapper.get_metadata()
        self.assertEqual(expected_meta, act_meta)

    def test_update_metadata(self):
        meta_mapper = MetadataMapper(self.container, "blah")
        meta_mapper._load_metadata = Mock(return_value={
            "change": {"name": "change", "value": "old", "immutable": False},
            "nono": {"name": "nono", "value": "old", "immutable": True}})
        meta_mapper._update_metadata({"change": {"name": "change", "value": "old", "immutable": False}})
        self.assertEqual(meta_mapper.change, {"name": "change", "value": "old", "immutable": False})
        meta_mapper._update_metadata({"nono": {"name": "nono", "value": "BAHA", "immutable": False}})
        self.assertEqual(meta_mapper.nono, {"name": "nono", "value": "old", "immutable": True})

    def test_remove_metadata(self):
        meta_mapper = MetadataMapper(self.container, "dublin/too/little")
        meta_mapper._load_metadata = Mock(return_value=utils.get_meta())
        meta_mapper.remove_metadata("tag")
        self.assertFalse(meta_mapper.item_exists("tag"))
        self.assertRaises(ImmutableMetadataError, meta_mapper.remove_metadata, "tag1")
        self.assertTrue(meta_mapper.item_exists("tag1"))
