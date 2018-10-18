#Based off of the alpine 3.7 image
FROM alpine:3.7

#Exposes port 8080 so that you can bind host ports to it
EXPOSE 8080
#Exposes the /srv/lanauth/config volume which lets you bind host folders to it
VOLUME /srv/lanauth/config
#Sets the working directory to /srv/lanauth/config
WORKDIR /srv/lanauth/config
#Sets the default value for the LANAUTH_CONFIG environment variable to prod.conf
ENV LANAUTH_CONFIG=prod.conf

#Install uwsgi, python3 and git in the container
RUN apk add --no-cache \
        uwsgi-python3 \
        python3 \
        git \
        openssl-dev \
        build-base \
        python3-dev \
        libffi-dev \
        openssh

#Installs the pylanauth git project as a python module
RUN pip3 install git+git://github.com/lsucs/pylanauth

#Runs uwsgi on port 8080 with the lanauth module
#LanAuth panel will be accessible from port 8080 in the container
CMD uwsgi \
		--http-socket :8080 \
		--plugins python3 \
		--module lanauth.__main__:uwsgi\(\) \
		--master --enable-threads
