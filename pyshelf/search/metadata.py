from elasticsearch_dsl import String, Nested, Boolean, DocType, tokenizer, analyzer


metadata_analyzer = analyzer("metadata_analyzer", tokenizer=tokenizer("keyword"))


class Metadata(DocType):
    items = Nested(
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
        self.items = metadata.values()
