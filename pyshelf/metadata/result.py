class Result(object):
    def __init__(self):
        self.error_code_list = []
        self.value = None

    @property
    def success(self):
        return not bool(len(self.error_code_list))

    def add_error(self, code):
        self.error_code_list.append(code)

    def has_error(self, code):
        has_error = False

        if code in self.error_code_list:
            has_error = True

        return has_error
