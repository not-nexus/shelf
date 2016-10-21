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

Health check only sets success or fail as they happen instead of every time the health check is called
------------------------------------------------------------------------------------------------------

For example, if AWS had an outage and then recovered, we may report failure even though we are actually able to connect. These inconsistencies are cleaned up as the API is used normally. We set the health of elasticsearch or an S3 bucket each time it is accessed.

This was done because one of the requirements for the health endpoint is that it would complete very quickly. There was some discussion surrounding creating a separate background process that would periodically do the checks itself and then allow our API processes to access its data via a socket but it started to get very complicated. For these reasons we accepted these possible inconsistencies as a risk.
