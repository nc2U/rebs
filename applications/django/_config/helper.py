import os
from django.core.exceptions import ImproperlyConfigured


def get_environment(var_name):
    """환경 변수를 가져오거나 예외를 반환한다."""
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)
