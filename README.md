# AlarmAbide
Temporarily disable all or specific alarms for specified amount of time (in seconds).

Can be imported as a module into alarms written in Python or can be used via
shell commands. Meant to be used to temporarily state an alarm is OK, even if
it may not be.

# Example using shell command for setting and removing, with bash script
checking (would be the bash script for alarm)

Disable resource1 alarm for 60 seconds
```bash
$ python alarmabide/alarmabide.py -c create -d /tmp/monitors/ -a test_alert -r resource1 -t 60
````

Run alarm check script and see that resource1 says its ok (default would be not ok in this script)
```bash
$ bash fake_alert_check.sh
First Check to see if we should alert for all
Continues to second check
OK for resource: resource1
Critical for resource: resource2
```

Disable resource2 alarm for 20 seconds
```bash
$ python alarmabide/alarmabide.py -c create -d /tmp/monitors/ -a test_alert -r resource2 -t 20
```

Run alarm check script, note that I ran this script within the 20 second and 60 second time frame
```bash
$ bash fake_alert_check.sh
First Check to see if we should alert for all
Continues to second check
OK for resource: resource1
OK for resource: resource2
```

Wait until the 20 and 60 second time expires and see everything alerts again
```bash
(venv)Davids-MacBook-Air:alarmabide dxjohnson$ bash fake_alert_check.sh
First Check to see if we should alert for all
Continues to second check
Critical for resource: resource1
Critical for resource: resource2
```

Set resource2 to not alert for 60 seconds, check it, then remove and check again.
```bash
$ python alarmabide/alarmabide.py -c create -d /tmp/monitors/ -a test_alert -r resource2 -t 60
$ bash fake_alert_check.sh
First Check to see if we should alert for all
Continues to second check
Critical for resource: resource1
OK for resource: resource2
$ python alarmabide/alarmabide.py -c remove -d /tmp/monitors/ -a test_alert -r resource2
$ bash fake_alert_check.sh
First Check to see if we should alert for all
Continues to second check
Critical for resource: resource1
Critical for resource: resource2
```