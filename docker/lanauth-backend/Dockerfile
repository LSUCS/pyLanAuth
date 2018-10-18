#Based off of the alpine 3.7 image
FROM alpine:3.7

#Exposes the /srv/lanauth/config volume which lets you bind host folders to it
VOLUME /srv/lanauth/config
#Sets the working directory to /srv/lanauth/config
WORKDIR /srv/lanauth/config
#Sets the default value for the LANAUTH_CONFIG environment variable to prod.conf
ENV LANAUTH_CONFIG=prod.conf

#Install python3, git and openssh in the container
RUN apk add --no-cache \
		openssl-dev \
		build-base \
		python3-dev \
		libffi-dev \        
		python3 \
    	git \
    	openssh

#Installs the pylanauth git project as a python module
RUN pip3 install git+git://github.com/lsucs/pylanauth

#Runs the lanauth daemon
CMD lanauth -c prod.conf daemon
