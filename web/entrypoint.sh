#!/bin/sh

# By default start up apache in the foreground, override with /bin/bash for interative.
exec /usr/sbin/apache2ctl -D FOREGROUND
