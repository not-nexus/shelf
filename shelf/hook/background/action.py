from shelf.logger_creator import LoggerCreator
from shelf.hook.background.container import Container
import json


def execute_command(command, log_level, event, uri, meta_uri, cwd="."):
    """
        Entry point to execute a command hook.

        Args:
            command(string) The command to execute. This can include arguments.
            log_level(int) One of the log levels defined on the logging module.
            event(string) The event that triggered this action. Should be one of
                shelf.hook.event.Event
            uri(string) The full URI to the artifact that was affected by the event.
            meta_uri(string) The full URI to the artifacts metadata resource.
            cwd(string) The directory we want to start at when executing the command.

        Returns:
            bool If we were successful or not.
    """
    container = create_container(log_level)
    logger = container.logger
    runner = container.create_command_runner(cwd)
    environment = {
        "SHELF_EVENT": event,
        "SHELF_URI": uri,
        "SHELF_META_URI": meta_uri
    }

    logger.info("Executing command \"{0}\" with environment data '{1}'".format(
        command,
        json.dumps(environment, indent=4)
    ))
    result = runner.run(command, environment)

    if result.success:
        logger.info("Command \"{0}\" executed successfully.".format(command))
    else:
        logger.error("Command \"{0}\" failed. stdout=\"{1}\" stderr=\"{2}\"".format(
            command,
            result.stdout,
            result.stderr
        ))

    return result.success


def create_container(log_level):
    logger = create_background_logger(log_level)
    container = Container(logger)

    return container


def create_background_logger(level):
    return LoggerCreator("BackgroundAction") \
        .background_format() \
        .level(level) \
        .get()
