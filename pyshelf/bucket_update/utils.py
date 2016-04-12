from pyshelf.bucket_update.container import Container
import logging
import os.path


def update_search_index(bucket_config):
    """
        Updates the search index for a specific bucket.

        Args:
            bucket_config(schemas/search-bucket-update-config.json)
    """
    container = _create_container(bucket_config)
    container.search_updater.run()


def _create_container(bucket_config):
    filename = os.path.join(bucket_config["bulkUpdateLogDirectory"], "{0}.log".format(bucket_config["name"]))
    logging.basicConfig(
        format="%(asctime)s:%(name)s:%(levelname)s:%(message)s",
        filename=filename,
        level=bucket_config["logLevel"],
    )
    logger = logging.getLogger(bucket_config["name"])
    container = Container(bucket_config, logger)
    return container
