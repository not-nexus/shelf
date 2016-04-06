class Context(object):
    def __init__(self):
        self.link_list = []
        self.error_list = []

    def add_link(self, link):
        self.link_list.append(link)

    def add_error(self, code):
        """
            Adds error to context.

            Args:
                code(pyshelf.error_code.ErrorCode)
        """
        self.error_list.append(code)

    def has_error(self):
        return len(self.error_list) > 0
