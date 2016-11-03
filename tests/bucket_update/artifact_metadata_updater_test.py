from tests.bucket_update.test_base import TestBase
from shelf.resource_identity import ResourceIdentity
from shelf.bucket_update.artifact_metadata_updater import ArtifactMetadataUpdater
from tests.metadata_builder import MetadataBuilder
from shelf.metadata.keys import Keys


class ArtifactMetadataUpdaterTest(TestBase):
    def test_run_initialization_always(self):
        """
            Important that whenever this runs it always
            reinitializes.  Specifically this is because
            somebody may change the referenceName.  In that
            case it must be updated to be the new artifactPath
        """
        path = "/test/artifact/my/fake/path"
        identity = ResourceIdentity(path)
        metadata = {
            "lol": {
                "name": "lol",
                "value": "whatever",
                "immutable": False,
            },
            Keys.PATH: {
                "name": Keys.PATH,
                "value": "/testing-api-bucket/artifact/my/fake/path",
                "immutable": True
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

        expected_artifact_path = {
            "name": Keys.PATH,
            "value": path,
            "immutable": True
        }
        self.assertEqual(expected_artifact_path, new_metadata["artifactPath"])

        self.assertEqual(updater.metadata, new_metadata)
