Bulk Update
===========

Update Search Index
-------------------

Even though we update metadata in both the cloud and the search index when new metadata comes in
there are situations where the search index could get out of sync with the source of truth (the metadata in the cloud).
Somebody could manually alter something in S3 or somebody could have added a completely new bucket.  In this case
we can use the `update-search-index.py` script in the `bin` directory.

It has the ability to update all, a few, or just one bucket.  For usage instructions see the help.

```
./bin/update-search-index.py --help
```
