class custom_value_error(ValueError):
    def __init__(self, arg):
        self.strerror = arg
        self.args = {arg}