from pyshelf.search.metadata import Metadata
from pyshelf.search import utils
import yaml
import os


class ElasticInitializer(object):
    def __init__(self, config_path):
        self.config_path = config_path

    def initialize(self):
        config = self.read_config()
        wrapper = utils.configure_es_connection(config["connectionString"],
                config.get("accessKey"), config.get("secretKey"), config.get("region"))
        Metadata.init(using=wrapper.connection, index=wrapper.index)
        self.es.indices.refresh(index=wrapper.index)

    def read_config(self):
        with open(self.config_path) as cf:
            config = yaml.load(cf.read())

            return config.get("elasticsearch")

bin_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.realpath(os.path.join(bin_dir, "../config.yaml"))
elastic = ElasticInitializer(config_path)
elastic.initialize()
