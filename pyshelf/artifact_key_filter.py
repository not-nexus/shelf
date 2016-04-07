import re
import os.path


def metadata(key_list):
    """
        Filters out keys that are metadata only.

        Args:
            key_list(List(s3.boto.key.Key))

        Returns:
            List(s3.boto.key.Key)
    """
    new_list = filter(_is_not_metadata, key_list)
    return new_list


def not_metadata(key_list):
    """
        Filter anything that is NOT metadata

        Args:
            key_list(List(s3.boto.key.Key))

        Returns:
            List(s3.boto.key.Key)
    """
    new_list = filter(_is_metadata, key_list)
    return new_list


def all_private(key_list):
    """
        Filters everything considered "private" and
        also metadata artifacts

        Args:
            key_list(List(s3.boto.key.Key))

        Returns:
            List(s3.boto.key.Key)
    """
    new_list = metadata(key_list)
    new_list = private(new_list)
    return new_list


def private(key_list):
    """
        Filters out keys that start with a directory
        that begins with an underscore (for instance
        things like "_keys" or "/blah/_hi".  This does
        NOT filter out metadata, even though they
        start with an underscore as well.

        Args:
            key_list(List(s3.boto.key.Key))

        Returns:
            List(s3.boto.key.Key)
    """
    new_list = filter(_is_not_private, key_list)
    return new_list


def _is_not_metadata(key):
    return not _is_metadata(key)


def _is_metadata(key):
    # Gets the last part of the artifact
    # path and makes sure it doesn't start
    # with _metadata
    name = os.path.split(key.name)[1]
    return bool(re.search("^_metadata", name))


def _is_not_private(key):
    return not _is_private(key)


def _is_private(key):
    # If it starts with an underscore or
    # any of the parts of the path start
    # with an underscore it is considered
    # private
    return bool(re.search("^_|/_(?!metadata)", key.name))
