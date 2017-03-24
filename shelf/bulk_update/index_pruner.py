import os
from shelf.search.update_manager import UpdateManager
from shelf.search.connection import Connection
from shelf.metadata.keys import Keys as MetadataKeys


class IndexPruner(object):
    """
        Prunes old documents from the Elasticsearch index.
    """
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        es_conf = self.config["elasticsearch"]
        connection = Connection(
            es_conf["connectionString"],
            access_key=es_conf.get("accessKey"),
            secret_key=es_conf.get("secretKey"),
            region=es_conf.get("region"))

        self.update_manager = UpdateManager(logger, connection)

    def run(self):
        """
            Runs search index cleaning process.
        """
        path_list = []

        for bucket in self.config["buckets"]:
            path = os.path.join("/" + bucket["referenceName"], "artifact/*")
            path_list.append(path)
            self.logger.info("Building path for {0}. {1}".format(bucket["referenceName"], path))

        response = self.update_manager.remove_unlisted_documents_wildcard(MetadataKeys.PATH, path_list)
        self.logger.info("Successfuly cleaned search index. {0} old documents deleted".format(response))
