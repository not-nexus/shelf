import logging
import sys
from pyshelf.request_log_filter import RequestLogFilter
import yaml
from pyshelf import utils


def app_config(existing_config, config_path):
    with open(config_path, "r") as f:
        content = f.read()
        config = yaml.load(content)

    utils.validate_json("schemas/config.json", config)

    if not config.get("bulkUpdateLogDirectory"):
        config["bulkUpdateLogDirectory"] = "/var/log/bucket-update"

    existing_config.update(config)


def logger(logger, log_level_name):
    log_level_name = log_level_name.upper()
    log_level = logging.getLevelName(log_level_name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s %(user)s%(request_id)s%(url)s- %(message)s")
    handler.setFormatter(formatter)
    handler.addFilter(RequestLogFilter())
    logger.addHandler(handler)
    logger.setLevel(log_level)
