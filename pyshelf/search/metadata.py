from elasticsearch_dsl import String, Nested, Boolean, DocType, tokenizer, analyzer


# Required for case sensitivity
metadata_analyzer = analyzer("metadata_analyzer", tokenizer=tokenizer("keyword"))


class Metadata(DocType):
    property_list = Nested(
        properties={
            "name": String(),
            "value": String(analyzer=metadata_analyzer),
            "immutable": Boolean()
        }
    )

    def update_all(self, metadata):
        """
            Updates all metadata related to an artifact.

            Args
                metadata(dict): collection of metadata for document.
        """
        self.property_list = metadata.values()
