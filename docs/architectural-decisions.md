Architectural Decisions
=======================

This document exists to document some decisions that were made that may appear strange or that were large design choices.

Search and Cloud Layers
-------------------------

We made an explicit decision to keep the "search" and "cloud" directories to be as decoupled from the rest of the code as possible.  At the moment, this only works with elasticsearch and S3 but the long term goal was to turn those "layers" into plugins.  Although we should always keep things as decoupled as possible, we should take special care with these.

Sorting and some searching is by the API instead of in Elasticsearch
--------------------------------------------------------------------

Currently, the sorting, the limiting and some of the searching for the [search functionality](api/search.md) is done by our API.  This was done for two reasons.

1. The metadata in Elasticsearch is structured in such a way that we can't sort on it.  This was an oversight and we have [an issue](https://github.com/kyle-long/pyshelf/issues/72) logged of just this thing.
2. [Version sort/search](api/search.md). Stock Elasticsearch does not seem to have this capability (especially the specific rules for how we wanted it to work).
