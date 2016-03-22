from elasticsearch_dsl import String, Nested, Boolean, DocType


class Metadata(DocType):
    key = String()
    items = Nested(
        properties={
            "name": String(),
            "value": String(),
            "immutable": Boolean()
        }
    )

    def add_item(self, item_key, item):
        self.items.append(item)
