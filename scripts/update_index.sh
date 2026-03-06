#!/bin/sh

sleeptime=15m # Sleep for 15 minutes after a failed try.
maxtries=3    # 3 * 15 minutes = about 45 minute total of waiting,
              # not counting running and failing.
cd /opt/scripts/
while ! (/usr/bin/python3 /opt/scripts/update_index.py >> /var/logs/update_index.log 2>&1); do
        maxtries=$(( maxtries - 1 ))
        if [ "$maxtries" -eq 0 ]; then
                echo Failed >&2
                exit 1
        fi

        sleep "$sleeptime" || break
done