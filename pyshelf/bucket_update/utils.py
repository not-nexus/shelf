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
    log_level = bucket_config["logLevel"]
    _configure_logger("elasticsearch", filename, log_level)
    logger = _configure_logger(bucket_config["name"], filename, log_level)
    container = Container(bucket_config, logger)
    return container


def _configure_logger(name, filename, log_level):
    logger = logging.getLogger(name)
    handler = logging.FileHandler(filename)
    formatter = logging.Formatter(fmt="%(asctime)s:%(name)s:%(levelname)s:%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger
