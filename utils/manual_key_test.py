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
    kn = "testing manual"
    key = bucket.get_key(kn)
    if key is not None:
        key.delete()
    key = bucket.new_key(kn)
    key.set_metadata('test', 'test value')
    key.set_metadata('test2', 'test value')
    key.set_contents_from_string("testing the manual setting of key.... wonder if it worked?!?!?!")
    key.open_read()
    print key
    
    print key.get_metadata('test')
    print key.metadata['test']
    print key.metadata
    conn.close()
