from elasticsearch_dsl import String, Nested, Boolean, DocType


class Metadata(DocType):
    items = Nested(
        properties={
            "name": String(),
            "value": String(),
            "immutable": Boolean()
        }
    )

    def update_all(self, metadata):
        """
            Updates all metadata related to an artifact.

            Args
                metadata(dict): collection of metadata for document.
        """
        self.items = metadata.values()
