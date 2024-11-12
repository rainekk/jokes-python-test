FROM alpine:3.11
MAINTAINER info@cstan.io

# add base and community repositories
ADD repositories /etc/apk/repositories
RUN apk add --update python py-pip@community

# install dependencies
RUN pip install flask

# create application directory
RUN mkdir -p /opt/joke_api/joke_api
ADD joke_api /opt/joke_api/joke_api
ADD entrypoint.sh /opt/joke_api/entrypoint.sh

# volume configuration
VOLUME ["/opt/joke_api/instance"]

# start application
CMD "/opt/joke_api/entrypoint.sh"

# listen on port 5000
EXPOSE 5000
