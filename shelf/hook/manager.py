from shelf.hook.event import Event
from shelf.hook.background import action


class Manager(object):
    def __init__(self, container, multiprocessing, host, command):
        """
            Args:
                container(shelf.hook.container)
                multiprocessing(multiprocessing)
                host(string) The protocol + hostname which hosts shelf.
                command(string) Command to run for each event.
        """
        self.container = container
        self.multiprocessing = multiprocessing
        self.host = host
        self.command = command

    def notify_artifact_uploaded(self, identity):
        """
            Should be called when an artifact is uploaded.

            Args:
                identity(shelf.resource_identity)
        """
        self._notify(identity, Event.ARTIFACT_UPLOADED)

    def notify_metadata_updated(self, identity):
        """
            Should be called when an artifact's metadata is updated.
            This will notify any hooks that are listening.

            Args:
                identity(shelf.resource_identity)
        """
        self._notify(identity, Event.METADATA_UPDATED)

    def _notify(self, identity, event):
        # I am assured that the identity's properties
        # will always begin with a "/" and the host
        # will NOT end in one.
        # Because the identity's properties start with "/"
        # os.path.join will not work.
        uri = self.host + identity.resource_url
        meta_uri = self.host + identity.metadata
        data = {
            "command": self.command,
            "event": event,
            "uri": uri,
            "meta_uri": meta_uri,
            "log_level": self.container.logger.level
        }

        process = self.multiprocessing.Process(target=action.execute_command, kwargs=data)
        process.start()
