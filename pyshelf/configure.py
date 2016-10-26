from jsonschema import ValidationError
from pyshelf import utils
from pyshelf.health import Health
from pyshelf.request_log_filter import RequestLogFilter
import logging
import multiprocessing
import os
import sys
import yaml


def app_config(existing_config, config_path):
    try:
        with open(config_path, "r") as f:
            content = f.read()
            config = yaml.load(content)
    except IOError:
        raise ValueError("Could not find or open file {0}".format(config_path))
    except:
        raise ValueError("{0} contained invalid yaml".format(config_path))

    try:
        utils.validate_against_schema("schemas/config.json", config)
    except ValidationError:
        raise ValueError(
            "{0} did not pass validation of json schema at schemas/config.json."
            " The original ValidationError was swallowed to prevent logging of sensitive data.".format(config_path)
        )
    utils.validate_bucket_config(config)
    config = utils.assign_reference_name(config)

    if not config.get("bulkUpdateLogDirectory"):
        config["bulkUpdateLogDirectory"] = "/var/log/bucket-update"

    existing_config.update(config)


def app_health(app):
    manager = multiprocessing.Manager()
    app.health = Health(app.config, manager)


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


def app(app):
    config_path = os.path.dirname(os.path.realpath(__file__)) + "/../config.yaml"
    app_config(app.config, config_path)
    app_health(app)
    log_level_name = app.config.get("logLevel", "DEBUG")
    logger(app.logger, log_level_name)
