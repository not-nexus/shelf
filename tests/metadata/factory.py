from shelf.metadata.yaml_codec import YamlCodec
from shelf.metadata.mapper import Mapper
from shelf.metadata.cloud_portal import CloudPortal
from shelf.cloud.storage import Storage


class Factory(object):
    def __init__(self, logger):
        self.logger = logger

    def create_fake_container(self, bucket_name=None):
        # Trailing comma in the tuple is important otherwise it is interpretted
        # as a grouping and just returns the type "object"
        fake_container = type("FakeMetadataContainer", (object,), {})()
        fake_container.yaml_codec = YamlCodec()
        fake_container.mapper = Mapper()
        fake_container.create_cloud_storage = lambda: Storage(None, None, bucket_name, self.logger)

        return fake_container

    def create_cloud_portal(self, bucket_name):
        container = self.create_fake_container(bucket_name)
        cloud_portal = CloudPortal(container)

        return cloud_portal
