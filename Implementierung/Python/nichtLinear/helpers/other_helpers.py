import inspect


def get_current_method_name(level=1):
    current_method_name = inspect.stack()[level][3]
    return current_method_name
