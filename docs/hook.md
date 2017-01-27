Hooks
=====

Hooks allow you to execute a script when certain events happen within shelf.

| Event               | Description                            |
|---------------------|----------------------------------------|
| `ARTIFACT_UPLOADED` | When any artifact is uploaded to shelf |
| `METADATA_UPDATED`  | Metadata was updated for any artifact  |

To [configure](configuration.md) shelf to use you script use the `hookCommand` property.

Your script will be executed with several environment vairables set.

| Environment Variable | Description                                                                                                                                                      |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `SHELF_EVENT`        | One of the above event values.                                                                                                                                   |
| `SHELF_URI`          | The full URI to the artifact that was affected by the event.                                                                                                     |
| `SHELF_META_URI`     | The full URI to the metadata link for the `SHELF_URI`.                                                                                                           |

Example
-------

	#!/usr/bin/env bash
	declare data

	# In this example I only care about ARTIFACT_UPLOADED I guess.
	if [[ "$SHELF_EVENT" != ARTIFACT_UPLOADED ]]; then
		exit 0
	fi

	data="{
		\"event\": \"$SHELF_EVENT\",
		\"uri\": \"$SHELF_URI\",
		\"metaUri\": \"$SHELF_META_URI\"
	}"

	# Tell somebody about our event. In this example we use google (which will always fail).
	statusCode=$(curl --out /dev/null -X POST --write-out "%{http_code}" --data "$data" www.google.com)

	# I'm expecting the status code to be somewhere in the 200 range for success.
	if [[ "$statusCode" -gt 299 || "$statusCode" -lt 200 ]]; then
		# Message to stderr which will get logged.
		echo "We've failed!" >&2

		# Exit with a non zero status code to signal failure.
		exit 1
	else
		# Message to stdout which will also get logged.
		echo "We've succeeded!"
	fi
