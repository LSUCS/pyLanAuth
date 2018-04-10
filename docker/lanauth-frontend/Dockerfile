FROM alpine:3.7

EXPOSE 8080
VOLUME /srv/lanauth/config
WORKDIR /srv/lanauth/config
ENV LANAUTH_CONFIG=prod.conf

RUN apk add --no-cache \
        uwsgi-python3 \
        python3 \
        git

RUN pip3 install git+git://github.com/lsucs/pylanauth

CMD uwsgi \
		--http-socket :8080 \
		--plugins python3 \
		--module lanauth.__main__:uwsgi\(\) \
		--master --enable-threads