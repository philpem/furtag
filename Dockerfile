#
# Dockerfile for Archivist
#

FROM python:3.7-alpine

COPY requirements.txt /

RUN set -e; \
	apk update \
	&& apk add --virtual .build-deps gcc libffi-dev python3-dev musl-dev \
	&& pip install --no-cache-dir -r /requirements.txt \
	&& pip install gunicorn \
	&& apk del .build-deps
RUN pip install sqltap

ADD . /app
WORKDIR /app

EXPOSE 8000
#CMD ["gunicorn", "-b", "0.0.0.0:8000", "myapp.app"]

VOLUME /var/lib/myapp

COPY Dentrypoint.sh /usr/local/bin
ENTRYPOINT [ "Dentrypoint.sh" ]
