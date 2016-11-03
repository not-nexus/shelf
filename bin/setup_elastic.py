from shelf.search.metadata import Metadata
import os
from shelf.search.connection import Connection
from shelf import configure


class ElasticInitializer(object):
    def __init__(self, config_path):
        self.config_path = config_path

    def initialize(self):
        config = self.read_config()
        connection = Connection(config["connectionString"],
                                config.get("accessKey"),
                                config.get("secretKey"),
                                config.get("region"))

        index_exists = connection.indices.exists(index=connection.es_index)

        if not index_exists:
            Metadata.init(using=connection, index=connection.es_index)

        connection.indices.refresh(index=connection.es_index)

    def read_config(self):
        config = {}
        configure.app_config(config, self.config_path)

bin_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.realpath(os.path.join(bin_dir, "../config.yaml"))
elastic = ElasticInitializer(config_path)
elastic.initialize()
