import os.path


class ArtifactPathBuilder(object):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def build(self, path):
        """
            Attempts to build an artifact path in only a single place.

            Note: I use this outside of an application context so I couldn't
            use flask url_for functionality.

            Args:
                path(basetring): The path as it would appear as the cloud
                    identifier.

            Returns:
                basestring: Full resource url.  For example:
                    /my-bucket/artifact/path/to/artifact/in/cloud
        """
        if path[0] == "/":
            path = path[1:]

        url = os.path.join("/" + self.bucket_name, "artifact", path)
        return url
