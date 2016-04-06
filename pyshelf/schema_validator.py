from jsonschema import validate
import json


class SchemaValidator(object):
    def __init__(self, logger):
        self.logger = logger

    def validate(self, data, schema_path):
        """
            Validates data against schema. This supresses all exceptions and merely returns True
            on success and False on failure. It also logs the details of the exception.

            Args:
                data(type outlined by schema_name)
                schema_path(string)

            Returns:
                bool: if data does not match schema
        """
        path = "schemas/{0}".format(schema_path)

        try:
            with open(path, "r") as file:
                schema = file.read()

            schema = json.loads(schema)
            validate(data, schema)
        except Exception as e:
            self.logger.exception(e)
            return False

        return True
