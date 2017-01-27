class CommandRunner(object):
    def __init__(self, logger, subprocess, CommandResult, cwd="."):
        """
            On the "cwd", this is the directory we start at. For example,
            if we have a script in "/script/hello.sh" we could set the
            cwd to "/script" and the command could just be "./hello.sh"

            Args:
                logger(logging.Logger)
                subprocess(subprocess)
                cwd(string) The "current working directory".
                CommandResult(class) The class defined in shelf.hook.command_result.
        """
        self.logger = logger
        self.subprocess = subprocess
        self.cwd = cwd
        self.CommandResult = CommandResult

    def run(self, command, env):
        """
            Executes a command.

            Args:
                command(string)
                env(dict) A dictionary of key value pairs. The key
                    will be the variable name.

            Returns:
                shelf.hook.command_result.CommandResult
        """
        command = command.split(" ")

        process = self.subprocess.Popen(
            command,
            cwd=self.cwd,
            env=env,
            stdout=self.subprocess.PIPE,
            stderr=self.subprocess.PIPE
        )

        stdout, stderr = process.communicate()
        exit_code = process.returncode

        result = self.CommandResult(stdout, stderr, exit_code)
        self.logger.debug("Command Result: {0}".format(result))

        return result
