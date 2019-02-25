FROM ubuntu:latest
MAINTAINER Nargiza Sarkulova

RUN apt update && apt -y upgrade && DEBIAN_FRONTEND=noninteractive apt -y install curl git sudo apache2 gnupg gnupg2 gnupg1

RUN DEBIAN_FRONTEND=noninteractive apt -y install build-essential

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -

RUN apt-get install -y nodejs

# Move localinfo to apache core directory
ADD ./ /var/www/html/localinfoweb

# Expose apache
EXPOSE 80

# By default start up apache in the foreground, override with /bin/bash for interative.
ADD entrypoint.sh /opt/entrypoint.sh

RUN chmod +x /opt/entrypoint.sh

CMD /opt/entrypoint.sh
