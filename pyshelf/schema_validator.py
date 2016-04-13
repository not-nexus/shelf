from jsonschema import validate
import json
import pyshelf.utils as utils


class SchemaValidator(object):
    def __init__(self, logger):
        self.logger = logger

    def validate(self, data, schema_path):
        """
            Validates data against schema. Logs and reraises any exceptions that occur.

            Args:
                data(type outlined schema)
                schema_path(string)

            Raises:
                ValidationError: if data does not match schema
                IOError: if schema_path is invalid
                SchemaError: if schema is flawed
        """
        schema_path = utils.create_path(schema_path)
        try:
            with open(schema_path, "r") as file:
                schema = file.read()

            schema = json.loads(schema)
            validate(data, schema)
        except Exception as e:
            self.logger.exception(e)
            # Log then reraise exception
            raise

    def format_error(self, error):
        """
            Formats ValidationError into a human readable error.

            Args:
                error(ValidationError)
            Returns:
                string: formatted error message.
        """
        msg_list = [error_item.message for error_item in error.context]
        msg = ", ".join(msg_list)

        return msg
