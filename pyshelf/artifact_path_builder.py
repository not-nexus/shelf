from flask import url_for


class ArtifactPathBuilder(object):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def build(self, path):
        """
            Builds the path part of the full url for an artifact.

            Note: This is tightly coupled with the name of the function in
            the artifact route which is terrible.  It seems to be the way
            to do it?  The point of making this object was to centralize the
            pain so that if we change that function name we only need to
            change it in a single place.
        """
        url = url_for(".get_path", path=path, bucket_name=self.bucket_name)
        return url
