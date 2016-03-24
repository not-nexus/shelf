from elasticsearch_dsl import String, Nested, Boolean, DocType


class Metadata(DocType):
    items = Nested(
        properties={
            "name": String(),
            "value": String(),
            "immutable": Boolean()
        }
    )

    class Meta:
        index="metadata"

    def update_all(self, metadata):
        """
            Updates all metadata related to an artifact.

            Args
                item(string): value to set the metdata item to.
        """
        self.items = metadata.values()
        self.save()

    def update_item(self, item):
        """
            Adds or updates an item in the metadata document distinguished by the unique key.

            Args
                item(string): value to set the metdata item to.
        """
        for ex_item in self.items:
            if item["name"] == ex_item["name"]:
                self.items.remove(ex_item)
        self.items.append(item)
        self.save()
