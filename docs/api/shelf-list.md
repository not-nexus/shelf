Shelf List
==========

This resource contains all the shelves (also called buckets or references) that you have access to.

`/`

GET
---

Retrieves all shelves you have access to.

The following headers are required.
| Name            | Type   | Description                                           |
|-----------------|--------|-------------------------------------------------------|
| `Authorization` | string | An authentication token which we can identify you by. |

**Response**

The response is an array of strings. Each string represents a "shelf" you have access to. The headers will contain links to `artifact-root` resources.

Examples
--------

	GET / HTTP/1.1
	Host: localhost:8080
	User-Agent: curl/7.47.0
	Accept: */*
	Authorization: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
	
	HTTP/1.1 200 OK
	Content-Type: application/json
	Link: </rick/artifact/>; rel="collection"; title="artifact-root"
	Link: </morty/artifact/>; rel="collection"; title="artifact-root"
	Content-Length: 18
	
	["rick", "morty"]
