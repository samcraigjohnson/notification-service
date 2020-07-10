import os


def is_dev():
    return _is_enivornment("dev")


def is_prod():
    return _is_enivornment("prod")


def is_test():
    return _is_enivornment("test")


def _is_enivornment(env):
    return os.environ.get("ENVIRONMENT").lower() == env.lower()
