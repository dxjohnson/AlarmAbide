#!/bin/bash
readonly ALERT_NAME='test_alert'
readonly MONITOR_DIRECTORY='/tmp/monitors'
echo "First Check to see if we should alert for all"
should_alert=$(/usr/bin/python alarmabide/alarmabide.py check $MONITOR_DIRECTORY $ALERT_NAME all)

if ! $should_alert; then
	echo "OK for alert $ALERT_NAME"
	exit 0
fi

echo "Continues to second check"

for resource in resource1 resource2; do
	should_alert=$(/usr/bin/python alarmabide/alarmabide.py check $MONITOR_DIRECTORY $ALERT_NAME $resource)

	if ! $should_alert; then
		echo "OK for resource: $resource"
	else
		echo "Critical for resource: $resource"
	fi
done
