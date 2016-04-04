class Result(object):
    def __init__(self):
        self.error_code_list = []
        self.value = None

    @property
    def success(self):
        """
            Figures out if the operation was successful.

            Returns:
                boolean
        """
        return not bool(len(self.error_code_list))

    def add_error(self, code):
        """
            Adds an error to the list.

            Args:
                code(pyshelf.metadata.error_code.ErrorCode)
        """
        self.error_code_list.append(code)

    def has_error(self, code):
        """
            Checks if we have a particular error code.

            Args:
                code(pyshelf.metadata.error_code.ErrorCode)

            Returns:
                boolean
        """
        has_error = (code in self.error_code_list)
        return has_error
