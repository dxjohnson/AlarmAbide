#!/usr/bin/env python
"""Alarm Abide

A module/script to be used in conjunction with other scripts/services and
    monitoring solutions to maintenance alert for a specified period of
    time.

Created By: David Johnson
"""

from datetime import datetime
from datetime import timedelta
import optparse
import os
import sys

class AlarmAbide(object):
    """Alarm Abide"""
    def __init__(self, directory):
        self.monitor_directory = directory

    def check(self, alert, resource):
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
                    self.remove(alert, resource)
        return True

    def create(self, alert, resource, time):
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

    def remove(self, alert, resource):
        """Remove alert file

        Remove file for given resource. Typically to be used on command line or
            by scripts, however also called by check if timestamp old.

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
    parser = optparse.OptionParser()
    parser.add_option('-a', '--alert', dest='alert')
    parser.add_option('-c', '--command', type='choice',
                      choices=['check', 'create', 'remove'], dest='command')
    parser.add_option('-d', '--directory', dest='directory', action='store')
    parser.add_option('-t', '--time', dest='time', action='store', type='int')
    parser.add_option('-r', '--resource', dest='resource', action='store')
    options, args = parser.parse_args()

    try:
        abide = AlarmAbide(options.directory)
        if options.command == "check":
            if abide.check(options.alert, options.resource):
                print "True"
            else:
                print "False"
        elif options.command == "create":
            abide.create(options.alert, options.resource, options.time)
        elif options.command == "remove":
            abide.remove(options.alert, options.resource)
    except Exception, err:
        print err
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())

