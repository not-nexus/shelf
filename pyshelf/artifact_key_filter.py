import re
import os.path


def to_path_list(key_list):
    """
        Turns a list of s3.boto.path.Key objects
        into a list of strings representing paths.

        Args:
            key_list(List(s3.boto.path.Key))

        Returns:
            List(basestring)
    """
    new_list = [key.name for key in key_list]
    return new_list


def metadata(path_list):
    """
        Filters out paths that are metadata only.

        Args:
            path_list(List(basestring))

        Returns:
            List(basestring)
    """
    new_list = filter(_is_not_metadata, path_list)
    return new_list


def not_metadata(path_list):
    """
        Filter anything that is NOT metadata

        Args:
            path_list(List(basestring))

        Returns:
            List(basestring)
    """
    new_list = filter(_is_metadata, path_list)
    return new_list


def all_private(path_list):
    """
        Filters everything considered "private" and
        also metadata artifacts

        Args:
            path_list(List(basestring))

        Returns:
            List(basestring)
    """
    new_list = metadata(path_list)
    new_list = private(new_list)
    return new_list


def private(path_list):
    """
        Filters out paths that start with a directory
        that begins with an underscore (for instance
        things like "_paths" or "/blah/_hi".  This does
        NOT filter out metadata, even though they
        start with an underscore as well.

        Args:
            path_list(List(basestring))

        Returns:
            List(basestring)
    """
    new_list = filter(_is_not_private, path_list)
    return new_list


def directories(path_list):
    """
        Filters out the path if we have identified
        it as a directory (ends with a "/")

        Args:
            path_list(List(basestring))

        Returns:
            List(basestring)
    """
    new_list = filter(_is_not_directory, path_list)
    return new_list


def is_reserved(path):
    """
        Determines if path is private or is metadata.

        Args:
            path(string)

        Returns:
            boolean: whether path is reserved or not.
    """
    reserved = bool(_is_private(path) or _is_metadata(path))
    return reserved


def _is_not_metadata(path):
    return not _is_metadata(path)


def _is_metadata(path):
    # Gets the last part of the artifact
    # path and makes sure it doesn't start
    # with _metadata
    name = os.path.split(path)[1]
    return bool(re.search("^_metadata", name))


def _is_not_private(path):
    return not _is_private(path)


def _is_private(path):
    # If it starts with an underscore or
    # any of the parts of the path start
    # with an underscore it is considered
    # private
    return bool(re.search("^_(?!metadata)|/_(?!metadata)", path))


def _is_not_directory(path):
    return not _is_directory(path)


def _is_directory(path):
    return bool(re.search("/$", path))
