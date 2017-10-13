"""
This module provides versioning informations.

    from SlackLogger.version import get_version
    __version__ = get_version()
"""

VERSION = '1.0.2'


def get_version():
    """
    Return package version value.

    :return: VERSION value, obviously
    :rtype: string
    """
    return VERSION
