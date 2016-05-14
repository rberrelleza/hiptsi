FROM gliderlabs/alpine:3.3

RUN apk add  --no-cache \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && virtualenv /env

COPY app /app
RUN  /env/bin/pip install -r /app/requirements.txt

EXPOSE 8080
VOLUME /data
CMD ["/env/bin/python", "/app/main.py"]
