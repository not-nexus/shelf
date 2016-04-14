import os.path
import json
import jsonschema


def create_path(*args):
    """
        Gets the full absolute path based on the arguments provided.  The part
        it adds at the beginning is the path to the root of this repository.

        WARNING: Do not start one of your path sections with a "/" otherwise that
        is expected to be an absolute path.

        Args:
            *args(List(basestring)): Each part is a segment of the same path.
    """
    directory_of_this_file = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(directory_of_this_file, "../", *args)
    full_path = os.path.realpath(full_path)
    return full_path


def validate_json(schema_path, data):
    """
        Validates data against schema.

        Args:
            schema_path(string)
            data(type outlined schema)

        Raises:
            jsonschema.ValidationError: if data does not match schema
            IOError: if schema_path is invalid
            jsonschema.SchemaError: if schema is flawed
    """
    schema_path = create_path(schema_path)
    with open(schema_path, "r") as file:
        schema = file.read()

    schema = json.loads(schema)
    jsonschema.validate(data, schema)
