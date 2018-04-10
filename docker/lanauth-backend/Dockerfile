FROM alpine:3.7

VOLUME /srv/lanauth/config
WORKDIR /srv/lanauth/config
ENV LANAUTH_CONFIG=prod.conf

RUN apk add --no-cache \
        python3 \
        git \
        openssh

RUN pip3 install git+git://github.com/lsucs/pylanauth

CMD lanauth -c prod.conf daemon