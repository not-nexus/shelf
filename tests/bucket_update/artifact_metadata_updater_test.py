from tests.bucket_update.test_base import TestBase
from pyshelf.resource_identity import ResourceIdentity
from pyshelf.bucket_update.artifact_metadata_updater import ArtifactMetadataUpdater
from tests.metadata_builder import MetadataBuilder
from pyshelf.metadata.keys import Keys


class ArtifactMetadataUpdaterTest(TestBase):
    def test_run_initialization_needed(self):
        path = "/test/artifact/my/fake/path"
        identity = ResourceIdentity(path)
        metadata = {
            "lol": {
                "name": "lol",
                "value": "whatever",
                "immutable": False,
            }
        }
        builder = MetadataBuilder(metadata)

        # Specifically setting it instead of
        # calling resource_url so that other
        # metadata is not generated
        builder._identity = identity
        self.add_cloud(builder)
        # Just need this to exist so the etag exists
        self.add_cloud_artifact(builder)

        actual_before_update = self.cloud_portal.load(identity.cloud_metadata)

        # Sanity check
        self.assertEqual(metadata, actual_before_update)

        updater = ArtifactMetadataUpdater(self.container.bucket_container, identity)
        updater.run()

        new_metadata = self.cloud_portal.load(builder.identity.cloud_metadata)
        expected_keys = [
            Keys.MD5,
            Keys.PATH,
            Keys.NAME,
        ]

        for key in expected_keys:
            if key not in new_metadata:
                self.fail("Key {0} was not initialized".format(key))
