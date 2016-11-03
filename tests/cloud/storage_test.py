import pyproctor
from shelf.cloud.storage import Storage
from mock import Mock


class StorageTest(pyproctor.TestBase):
    def test_key_map_cache(self):
        storage = Storage("key", "key", "bucket", Mock())
        get_key_mock = Mock(return_value="key")
        bucket_mock = type("FakeBucket", (), {"get_key": get_key_mock})
        storage._get_bucket = Mock(return_value=bucket_mock)
        storage._get_key("artifactName")
        storage._get_key("artifactName")
        storage._get_bucket.assert_called_once_with("bucket")
        get_key_mock.assert_called_once_with("artifactName")
