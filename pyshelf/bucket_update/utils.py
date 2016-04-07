from pyshelf.bucket_update.container import Container
import sys
import logging


def update_search_index(bucket_config):
    """
        Updates the search index for a specific bucket.

        Args:
            bucket_config(schemas/search-bucket-update-config.json)
    """
    container = _create_container(bucket_config)
    container.search_updater.run()


def _create_container(bucket_config):
    logging.basicConfig(stream=sys.stdout, level=bucket_config["logLevel"])
    logger = logging.getLogger(bucket_config["name"])
    container = Container(bucket_config, logger)
    return container
