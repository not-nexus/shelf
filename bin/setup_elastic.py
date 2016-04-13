from pyshelf.search.metadata import Metadata
from pyshelf.search import utils
import yaml


class ElasticInitializer(object):
    def __init__(self, config_path):
        self.config_path = config_path

    def initialize(self):
        config = self.read_config()
        connection, index = utils.configure_es_connection(config["connectionString"],
                config.get("accessKey"), config.get("secretKey"), config.get("region"))
        Metadata.init(using=connection, index=index)
        self.es.indices.refresh(index=index)

    def read_config(self):
        with open(self.config_path) as cf:
            config = yaml.load(cf.read())

            return config.get("elasticSearch")

elastic = ElasticInitializer("config.yaml")
elastic.initialize()
