Advanced Search Examples
========================

Searching for a particular version
----------------------------------

Since a version formatted value could be stored in any metadata property, if you would like to use the special version search you will need to use the `~` character.  You can still try to match on a version without the version search however.

**Search using the version search**

    POST /bucket-name/artifact/_search
    Authorization: supersecrettoken

    {
        "search": "version~=1.2"
    }

| Found | Not Found |
|-------|-----------|
| 1.2   | 1.1       |
| 1.9   | 2.0       |
| 1.9.9 | 1.1.9     |
| 1.2.1 | 2.0.1     |
| v1.2  | v2.0      |

**Search using wildcard**

    POST /bucket-name/artifact/_search
    Authorization: supersecrettoken

    {
        "search": "version=1.*"
    }


| Found                 | Not Found |
|-----------------------|-----------|
| 1.0                   | 0.1       |
| 1.9                   | 2.0       |
| 1.9.9                 | v1.0      |
| 1.myspecialversion    | x         |

**Equality search**

    POST /bucket-name/artifact/_search
    Authorization: supersecrettoken

    {
        "search": "version=1.0"
    }

| Found | Not Found             |
|-------|-----------------------|
| 1.0   | anything else         |


Getting the latest version
--------------------------

You can get the latest version of something by combining sort with limit. 

    
    POST /bucket-name/artifact/_search
    Authorization: supersecrettoken

    {
        "sort": "version, VER, DESC",
        "limit": 1
    }

Which will return a single link to an artifact.  This artifact was the first in all artifacts when sorted using the `VER` (`VERSION` can also be used) sort and sorting it `DESC` (`DESCENDING` can also be used).

You could also combine this with a sort.  You may want the latest version where it has been "tested" for instance.

    
    POST /bucket-name/artifact/_search
    Authorization: supersecrettoken

    {
        "search": "tested=true",
        "sort": "version, VER, DESC",
        "limit": 1
    }


Combined example
----------------

We can also sort multiple times and search for multiple things.

    POST /bucket-name/artifact/_search
    Authorization: supersecrettoken

    {
        "search": [
            "tested=true",
            "version~=1.1"
        ],
        "sort": [
            "version, VER, DESC",
            "buildNumber, DESC"
        ],
        "limit": 3
    }

To spell it out, we want:
* Artifacts that are tested
* Anything with a version higher than or equal to 1.1, but lower than 2
* Sort on the field "version" and treat it as a special VERSION field and sort by it desending
* Sort for buildNumber descending (as a secondary sort) 
* Only get three links back

The below table represent a sample set of artifacts (and what their metadata
is set to) that are sorted and specifying whether it meets the criteria in the above
search.

| tested       | version    | buildNumber      | Included (in the top 3) |
|--------------|------------|------------------|-------------------------|
| true ![][y]  | 1.9 ![][y] | 10 ![][y]        | ![][y]                  |
| true ![][y]  | 1.9 ![][y] | 9 ![][y]         | ![][y]                  |
| true ![][y]  | 1.8 ![][y] | 10 ![][y]        | ![][y]                  |
| true ![][y]  | 1.5 ![][y] | 8 ![][y]         | ![][n]                  |
| true ![][y]  | 2.0 ![][n] | 3 ![][y]         | ![][n]                  |
| true ![][y]  | 1.3 ![][y] | (not set) ![][n] | ![][n]                  |
| false ![][n] | 1.1 ![][y] | 5 ![][y]         | ![][n]                  |
| true ![][y]  | 1.0 ![][n] | 4 ![][y]         | ![][n]                  |

[y]: check.jpg
[n]: x.jpg
