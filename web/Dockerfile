FROM ubuntu:latest
MAINTAINER Nargiza Sarkulova

RUN apt update && apt -y upgrade && DEBIAN_FRONTEND=noninteractive apt -y install curl git sudo apache2

# Move localinfo to apache core directory
ADD public /var/www/html

# Manually set up the apache environment variables
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid

# Enable apache mods.
RUN a2enmod rewrite

# Update the default apache site with the config we created.
ADD apache/apache.conf /etc/apache2/sites-enabled/000-default.conf

# Expose apache
EXPOSE 80

# By default start up apache in the foreground, override with /bin/bash for interative.
ADD entrypoint.sh /opt/entrypoint.sh

RUN chmod +x /opt/entrypoint.sh
CMD /opt/entrypoint.sh
