from pyshelf.search.metadata import Metadata
import yaml
import os
from pyshelf.search.connection import Connection


class ElasticInitializer(object):
    def __init__(self, config_path):
        self.config_path = config_path

    def initialize(self):
        config = self.read_config()
        connection = Connection(config["connectionString"],
                config.get("accessKey"), config.get("secretKey"), config.get("region"))
        connection.indices.create(index=connection.es_index, ignore=400)
        Metadata.init(using=connection, index=connection.es_index, ignore=400)
        connection.indices.refresh(index=connection.es_index)

    def read_config(self):
        with open(self.config_path) as cf:
            config = yaml.load(cf.read())

            return config.get("elasticsearch")

bin_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.realpath(os.path.join(bin_dir, "../config.yaml"))
elastic = ElasticInitializer(config_path)
elastic.initialize()
