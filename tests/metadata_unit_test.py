from unit_test_base import UnitTestBase
from pyshelf.cloud.metadata_mapper import MetadataMapper
from mock import MagicMock
from moto import mock_s3
import boto
from boto.s3.key import Key
import yaml


class MetadataUnitTest(UnitTestBase):
    def _setup_metadata(self, artifact_name, metadata=None):
        exists = (metadata != None)
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
        self._setup_metadata("non_existant")
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
            }
        }
        meta_mapper.set_metadata(meta)
        item = meta_mapper.get_metadata("metaItem")
        self.assertEqual(item, {"value": "this is most certainly new", "immutable": False})
        meta_mapper.set_metadata({"value": "lolol", "immutable": True}, "metaItem")
        act_meta = meta_mapper.get_metadata()
        self.assertEqual(expected_meta, act_meta)
