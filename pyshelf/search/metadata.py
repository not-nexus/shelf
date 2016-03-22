from elasticsearch_dsl import String, Nested, Boolean, DocType


class Metadata(DocType):
    items = Nested(
        properties={
            "name": String(),
            "value": String(),
            "immutable": Boolean()
        }
    )

    def add_item(self, item_key, item):
        """
            Adds or updates an item in the metadata doc distinguished by the unique key.

            Args
                item_key(string): key of metadata item.
                item(string): value to set the metdata item to.
        """
        # Seems like this is pointless but I can imagine the functionality of this
        # function growing... but perhaps not
        self.items.update({item_key: item})
