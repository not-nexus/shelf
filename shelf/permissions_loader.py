import yaml
from shelf.cloud.cloud_exceptions import ArtifactNotFoundError


class PermissionsLoader(object):
    def __init__(self, logger, cloud_factory):
        """
            Args:
                logger(logging.Logger)
                cloud_factory(shelf.cloud.factory.Factory)
        """
        self.cloud_factory = cloud_factory
        self.logger = logger

    def load(self, bucket, token):
        """
            Gets the contents of the token file (if it can be found) as
            a dict.

            Args:
                bucket(string)
                token(string)

            Returns:
                dict|None
        """
        permissions = None

        with self.cloud_factory.create_storage(bucket) as storage:
            try:
                token_file = storage.get_artifact_as_string("_keys/{0}".format(token))

                try:
                    permissions = yaml.load(token_file)
                except:
                    self.logger.info("Failed to decode the token file as YAML.")
            except ArtifactNotFoundError:
                self.logger.debug("Failed to find token provided.")

        return permissions
