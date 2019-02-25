#!/bin/sh

# By default start up apache in the foreground, override with /bin/bash for interative.
cd /var/www/html/localinfoweb && npm install
exec npm run server
