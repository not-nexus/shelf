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


def validate_against_schema(schema_path, data):
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


def get_bucket_config(config, bucket_name):
    """
        Pulls correct bucket config from application config based on name/alias.

        Args:
            config(dict)
            bucket_name(string): bucket name or bucket reference name

        Returns:
            dict | None: config for bucket or None if not found
    """
    bucket_config = None

    for bucket in config["buckets"]:
        if bucket_name == bucket["referenceName"]:
            bucket_config = bucket

    return bucket_config


def validate_bucket_config(config):
    """
        Verifies that there is no overlap in referance name and bucket name.

        Args:
            config(dict)

        Raises:
            ValueError
    """
    name_list = []

    for bucket in config["buckets"]:
        if bucket["name"] == bucket.get("referenceName") or bucket.get("referenceName") is None:
            name_list.append(bucket["name"])
        else:
            name_list.extend([bucket["name"], bucket["referenceName"]])

    unique_list = list(set(name_list))

    if len(name_list) != len(unique_list):
        raise ValueError("Error in bucket config. Overlapping bucket names and reference names.")


def assign_reference_name(config):
    """
        Assigns bucket name to reference name if reference name doesn't exist.

        Args:
            config(dict)

        Returns:
            dict: formatted config
    """
    for bucket in config["buckets"]:
        if bucket.get("referenceName") is None:
            bucket["referenceName"] = bucket["name"]

    return config
