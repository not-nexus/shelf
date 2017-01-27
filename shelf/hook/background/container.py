from shelf.hook.background.command_result import CommandResult
from shelf.hook.background.command_runner import CommandRunner
import subprocess


class Container(object):
    def __init__(self, logger):
        """
            Args:
                logger(logging.Logger)
                command(string)
        """
        self.logger = logger

    def create_command_runner(self, cwd="."):
        """
            Args:
                cwd(string)

            Returns:
                shelf.hook.command_runner.CommandRunner
        """
        runner = CommandRunner(
            self.logger,
            subprocess,
            CommandResult,
            cwd
        )

        return runner
