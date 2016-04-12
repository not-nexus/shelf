from pyshelf.search.metadata import Metadata
from elasticsearch import Elasticsearch
from urlparse import urlparse


class ElasticInitializer(object):
    def __init__(self, connection_string):
        parsed = urlparse(connection_string)
        url = parsed.scheme + "://" + parsed.netloc
        self.index = parsed.path[1:]
        self.es = Elasticsearch(url)

    def initialize(self):
        Metadata.init(using=self.ex, index=self.index)
        self.es.indices.refresh(index=self.index)


with open("config.yaml") as cf:
    config = cf.read()

elastic = ElasticInitializer(config.get("elasticSearchConnectionString"))
elastic.initialize()
