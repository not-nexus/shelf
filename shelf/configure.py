from jsonschema import ValidationError
from shelf.health import Health
from shelf import utils
from shelf.logger_creator import LoggerCreator
from shelf.request_log_filter import RequestLogFilter
import multiprocessing
import os
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

    if config.get("hookCommand"):
        config["hookCommand"] = hook_command(config_path, config["hookCommand"])

    existing_config.update(config)


def hook_command(config_path, cmd):
    # Making the hookCommand relative to to the configuration file.
    cmd = os.path.join(os.path.dirname(config_path), cmd)

    # To make it easier to understand
    cmd = os.path.realpath(cmd)

    # Get just the path to the file without any arguments if they exist
    # so that I can do a few checks below.
    #
    # Note: I just thought of a limitation where a filename or directory name
    # cannot have a space in it. Due to this being the "tactical" solution I
    # am not going to worry about it too much at the moment.
    # Problem Code: NO_SPACE_IN_FILENAME
    exe_path, _, _ = cmd.partition(" ")

    if not os.path.isfile(exe_path) or not os.access(exe_path, os.X_OK):
        raise ValueError("hookCommand's file \"{0}\" is either not a file or is not executable.".format(exe_path))

    return cmd


def app_health(app):
    manager = multiprocessing.Manager()
    app.health = Health(app.config, manager)


def logger(logger, log_level_name):
    LoggerCreator(logger).request_format().level_name(log_level_name).handler.addFilter(RequestLogFilter())


def app(app):
    config_path = os.path.dirname(os.path.realpath(__file__)) + "/../config.yaml"
    app_config(app.config, config_path)
    app_health(app)
    log_level_name = app.config.get("logLevel", "DEBUG")
    logger(app.logger, log_level_name)
