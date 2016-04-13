import os.path


def create_path(*args):
    """
        Gets the full absolute path based on the arguments provided.  The part
        it adds at the beginning is the path to the root of this repository.

        WARNING: Do not start one of your path sections with a "/" otherwise that
        is expected to be an absolute path.

        Args:
            *args(List(basestring)): Each part is a segment of the same path.
    """
    directory_of_this_file = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(directory_of_this_file, "../", *args)
    full_path = os.path.realpath(full_path)
    return full_path
