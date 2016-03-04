import yaml
from boto.s3.connection import S3Connection
from boto.s3.key import Key

with open("config.yaml", "r") as f:
    content = f.read()
    config = yaml.load(content)
    access_key = config.get("accessKey")
    secret_key = config.get("secretKey")
    bucket_name = config.get("bucketName")

    conn = S3Connection(access_key, secret_key)
    bucket = conn.get_bucket(bucket_name)
    # Test code below.
    test = list(bucket.list(prefix="", delimiter="/"))
    for t in test:
        print t.name
    conn.close()
