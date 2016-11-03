class Context(object):
    def __init__(self):
        self.link_list = []
        self.errors = {}

    def add_link(self, link):
        self.link_list.append(link)

    def add_error(self, code, message=None):
        """
            Adds error to context with optional message.

            Args:
                code(shelf.error_code.ErrorCode)
                message(string | None)
        """
        self.errors[code] = message

    def has_error(self):
        """
            Returns:
                boolean: whether error exists on context or not.
        """
        return len(self.errors) > 0
