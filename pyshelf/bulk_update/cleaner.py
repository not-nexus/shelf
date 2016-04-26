from pyshelf.bucket_update import utils


class Cleaner(object):
    """
        Takes care of cleaning old documents from the Elasticsearch index.
    """
    def __init__(self, container):
        self.container = container
        self.config = self.container.config

    def run(self):
        """
            Runs search index cleaning process.
        """
        id_list = self.bucket_container.search_updater.load_id_list()
        self.bucket_container.update_manager.remove_unlisted_documents(id_list)

    def load_id_list(self):
        id_list = []

        for bucket in self.config["buckets"]:
            # Creating bucket container per bucket
            c = utils.create_bucket_container(bucket, self.container.logger)
            path_list = c.search_updater.load_path_list()

            for path in path_list:
                identity = c.resource_identity_factory.from_cloud_identifier(path)
                id_list.append(identity.search)

        return id_list
