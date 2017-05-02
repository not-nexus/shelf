from shelf.bucket_update.container import Container
import os.path
from shelf import background_utils


def update_search_index(bucket_config):
    """
        Updates the search index for a specific bucket.

        Args:
            bucket_config(schemas/search-bucket-update-config.json)
    """
    container = _create_container(bucket_config)
    container.search_updater.update()


def prune_search_index(bucket_config):
    """
        Prunes the search index for a specific bucket.

        Args:
            bucket_config(schemas/search-bucket-update-config.json)
    """
    container = _create_container(bucket_config)
    container.search_updater.prune()


def _create_container(bucket_config):
    filename = os.path.join(bucket_config["bulkUpdateLogDirectory"], "{0}.log".format(bucket_config["name"]))
    log_level = bucket_config["logLevel"]
    background_utils.configure_file_logger("elasticsearch", filename, log_level)
    logger = background_utils.configure_file_logger(bucket_config["name"], filename, log_level)
    container = Container(bucket_config, logger)

    return container
