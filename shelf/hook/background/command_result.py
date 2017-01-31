import json


class CommandResult(object):
    """
        This class really only exists to be explicit about the interface
        but it's possible in the future we would want to add some helper
        functions. For example, decode stdout as json.
    """
    def __init__(self, stdout=None, stderr=None, exit_code=None):
        """
            Args:
                stdout(string)
                stderr(string)
                exit_code(int)
        """
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code

    @property
    def success(self):
        return self.exit_code == 0

    def __str__(self):
        string = json.dumps(
            self.__dict__,
            indent=4
        )

        return string
