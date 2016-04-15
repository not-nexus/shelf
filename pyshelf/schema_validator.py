import pyshelf.utils as utils


class SchemaValidator(object):
    def __init__(self, logger):
        self.logger = logger

    def validate(self, schema_path, data):
        """
            Validates data against schema. Logs and reraises any exceptions that occur.

            Args:
                schema_path(string)
                data(type outlined schema)

            Raises:
                jsonschema.ValidationError: if data does not match schema
                IOError: if schema_path is invalid
                jsonschema.SchemaError: if schema is flawed
        """
        try:
            utils.validate_json(schema_path, data)
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
