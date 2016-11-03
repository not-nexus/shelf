from pyshelf.metadata.keys import Keys
from datetime import datetime


class Initializer(object):
    """
        Responsible for dealing with initialization of
        metadata.  It is the single point where we

        1.) Determine what metadata should be initialized
        2.) Determine if metadata needs to be initialized
    """
    def __init__(self, container):
        """
            Args:
                container(pyshelf.metadata.container.Container)
        """
        self.container = container
        self.mapper = self.container.mapper

    def needs_update(self, metadata):
        """
            Determines if we should reinitialize the provided
            metadata

            Args:
                metadata(schemas/metadata.json)

            Returns:
                boolean
        """
        required = [
            Keys.MD5,
            Keys.PATH,
            Keys.NAME,
            Keys.CREATED_DATE
        ]

        needs_update = True
        # Sets use the iterable functionality of the thing passed to
        # it to build the set.  In the case of a dict it will return
        # the keys.  In the case of a List it will use the items.
        # This line checks to see if the required set is a not a subset
        # of the metadata keys.  In other words, if the required list has
        # a key that is not in the metadata set.
        if set(required) <= set(metadata):
            needs_update = False

        return needs_update

    def update(self, identity, metadata):
        """
            Updates the metadata to have the required keys.
            Note: This does not update it in the cloud.

            Args:
                metadata(schemas/metadata.json)
                resource(pyshelf.resource_identity.ResourceIdentity)

            Returns:
                metadata(schemas/metadata.json): But updated
        """
        with self.container.create_cloud_storage() as storage:
            etag = storage.get_etag(identity.cloud)
            metadata[Keys.MD5] = self.mapper.create_response_property(Keys.MD5, etag, True)

        if Keys.CREATED_DATE not in metadata:
            created = self._get_created_date()
            metadata[Keys.CREATED_DATE] = self.mapper.create_response_property(Keys.CREATED_DATE, created, True)

        metadata[Keys.PATH] = self.mapper.create_response_property(Keys.PATH, identity.resource_path, True)
        metadata[Keys.NAME] = self.mapper.create_response_property(Keys.NAME, identity.artifact_name, True)

        return metadata

    def _get_created_date(self):
        created_date = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        return created_date
