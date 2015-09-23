#!/usr/bin/env python
"""Alarm Abide

A module/script to be used in conjunction with other scripts/services and
    monitoring solutions to maintenance alert for a specified period of
    time.

Created By: David Johnson
"""

from datetime import datetime
from datetime import timedelta
import os
import sys

class AlarmAbide(object):
    """Alarm Abide"""
    def __init__(self, directory):
        self.monitor_directory = directory

    def check_alert(self, alert, resource):
        """Checks to see if an alert should occur

        Checks each of the possible paths to see if files exists for alert. If the
            file exist it checks and compares it to now(). Removes file if
            timestamp in file is old.

        Args:
            alert: Name of the alert (script)
            resource: Name of the resouce you are checking for
                'all' means for all resources or all alerts depending on location

        Returns:
            Returns False if a alert should not be tested
            Returns True if an alert should be tested

        Raises:
            Everything
        """
        paths = (
            os.path.join(self.monitor_directory, "all"),
            os.path.join(self.monitor_directory, alert, "all"),
            os.path.join(self.monitor_directory, alert, resource)
            )

        for path in paths:
            if os.path.isfile(path):
                with open(path, 'r') as alert_file:
                    time = alert_file.readline()
                time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                if time > datetime.now():
                    return False
                else:
                    self.remove_alert(alert, resource)

    def create_alert(self, alert, resource, time):
        """Create alert file

        Create a new alert file with now() + time in seconds for specified
            resource. Typically to be used on command line or by scripts.

        Args:
            alert: Name of the alert (script)
            resource: Name of the resouce you are checking for
                'all' means for all resources or all alerts depending on location
            time: time in seconds to keep alert hidden for

        Returns:
            Returns True if file created
            Returns False if file not created

        Raises:
            Everything
        """
        alert_time = datetime.now() + timedelta(seconds=time)
        alert_time = alert_time.replace(microsecond=0)
        path = os.path.join(self.monitor_directory, alert, resource)

        if not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

        with open(path, 'w') as alert_file:
            alert_file.write(str(alert_time))

    def remove_alert(self, alert, resource):
        """Remove alert file

        Remove file for given resource. Typically to be used on command line or
            by scripts, however also called by check_alert if timestamp old.

        Args:
            alert: Name of the alert (script)
            resource: Name of the resouce you are checking for
                'all' means for all resources or all alerts depending on location

        Returns:

        Raises:
            Everything
        """
        path = os.path.join(self.monitor_directory, alert, resource)
        os.remove(path)

def main():
    """Main function for command line use

    For use with scripts that are not Python and therefore can not import.

    Args:
        args[1]: Command to be ran
            Check - See if a alert should alarm or not
            Create - Disable a alert for specified time
            Remove - Remove alert file
        args[2]: Alert Name (found in path)
        args[3]: Resource such as socket
            If resource is 'all' then don't alert for anything
        args[4]: Specified time to not alert for (only for create)

    Returns:
        Check - prints true to standard out if alert should sound, false if not
        All exit 0 on sucess or 1 on failure

    Raises:
        Everything
    """
    try:
        command = sys.argv[1]
        directory = sys.argv[2]
        abide = AlarmAbide(directory)
        alert = sys.argv[3]
        resource = sys.argv[4]
        if command == "check":
            if abide.check_alert(alert, resource):
                print "True"
            else:
                print "False"
        elif command == "create":
            try:
                time = int(sys.argv[5])
            except:
                raise
            abide.create_alert(alert, resource, time)
        elif command == "remove":
            abide.remove_alert(alert, resource)
        elif command == "help":
            print "Usage: $0 check|create|remove directory <parameters>"
            print "$2 = directory to place check"
            print "$3 = alert, $4 = resource"
            print "For create: $5 = time in seconds"
        else:
            sys.stderr.write('ERROR: unknown option - %s\n' % command)
    except Exception, err:
        print err
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()

