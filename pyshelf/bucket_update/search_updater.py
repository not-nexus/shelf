import pyshelf.artifact_key_filter as filters
from pyshelf.bucket_update.artifact_metadata_updater import ArtifactMetadataUpdater
from pprint import pformat
import gc


class SearchUpdater(object):
    def __init__(self, container):
        self.container = container
        self.bucket_container = self.container.bucket_container
        self.chunk_size = self.container.config["chunkSize"]
        self.logger = self.container.logger
        self.update_manager = self.container.search_container.update_manager

    def load_path_list(self):
        with self.bucket_container.create_cloud_storage() as storage:
            artifact_list = storage.get_directory_contents("", True)
            artifact_list = filters.directories(artifact_list)
            artifact_list = filters.all_private(artifact_list)
            artifact_name_list = [key.name for key in artifact_list]

        return artifact_name_list

    def run(self):
        path_list = self.load_path_list()
        gc.collect()

        if not path_list:
            self.logger.info("Found nothing to process.")
            return

        self.logger.info("Starting to process {0} artifact's metadata".format(len(path_list)))
        all_id_list = []
        for chunk_list in self._chunk(path_list):
            bulk_update = {}
            self.logger.info("Processing chunk: {0}".format(pformat(chunk_list)))
            for path in chunk_list:
                self.handle_artifact(path, bulk_update)

            self.update_manager.bulk_update(bulk_update)
            all_id_list = all_id_list + bulk_update.keys()

        self.logger.info("Deleting anything in search that is not in this list {0}".format(pformat(all_id_list)))
        self.update_manager.remove_unlisted_documents_per_bucket(all_id_list, self.container.config["name"])
        self.logger.info("Update of bucket {0} has been completed".format(self.container.config["name"]))

    def handle_artifact(self, path, bulk_update):
        identity = self.container.resource_identity_factory \
            .from_cloud_identifier(path)
        updater = ArtifactMetadataUpdater(self.bucket_container, identity)
        updater.run()
        bulk_update[identity.search] = updater.metadata

    def _chunk(self, path_list):
        """
            A generate that will (with each yield) return the next
            chunk of artifact paths that should be processed
        """
        for index in range(0, len(path_list), self.chunk_size):
            yield path_list[index: index + self.chunk_size]

        yield path_list[index:]
