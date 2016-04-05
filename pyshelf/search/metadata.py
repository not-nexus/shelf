from elasticsearch_dsl import String, Nested, Boolean, DocType, tokenizer, analyzer


# Required for case sensitivity
# To add an analyzer to an existing mapping requires mapping to be "closed"
case_sensitive_analyzer = analyzer("case_sensitive_analyzer", tokenizer=tokenizer("keyword"))


class Metadata(DocType):
    property_list = Nested(
        properties={
            "name": String(analyzer=case_sensitive_analyzer),
            "value": String(analyzer=case_sensitive_analyzer),
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
