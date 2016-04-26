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
        id_list = []
        bucket_container = None

        for bucket in self.config["buckets"]:
            # Creating bucket container per bucket
            bucket.update({
                "elasticsearch": self.config["elasticsearch"]
            })
            bucket_container = utils.create_bucket_container(bucket, self.container.logger)
            path_list = bucket_container.search_updater.load_path_list()
            self.container.logger.debug("Gathering existant artifacts for {0}".format(bucket["referenceName"]))

            for path in path_list:
                identity = bucket_container.resource_identity_factory.from_cloud_identifier(path)
                id_list.append(identity.search)

        update_manager = bucket_container.search_container.update_manager
        response = update_manager.remove_unlisted_documents(id_list)
        self.container.logger.debug("Successfuly cleaned search index. {0} old documents deleted".format(response))
