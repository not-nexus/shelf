class NullManager(object):
    """
        This class exists to have the same interface as the
        shelf.hook.manager except do nothing. This will
        be used in the case that a "hookCommand" is not
        configured.
    """
    def notify_artifact_uploaded(self, identity):
        """
            Args:
                identity(shelf.resource_identity)
        """
        pass

    def notify_metadata_updated(self, identity):
        """
            Args:
                identity(shelf.resource_identity)
        """
        pass
