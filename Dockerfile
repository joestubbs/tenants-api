# image: tapis/tenants-api
from python:3.7

RUN useradd tapis
ADD requirements.txt /home/tapis/requirements.txt

RUN pip install -U --no-cache-dir pip && \
    pip install --no-cache-dir -r /home/tapis/requirements.txt

# TODO -- eventually remove this
RUN apt-get update && apt-get install -y vim

# ----Add the common lib (eventually this will be a pip install)
COPY common /usr/local/lib/python3.7/site-packages/common

WORKDIR /home/tapis

# ----API specific code
ENV TAPIS_API tenants
ENV FLASK_APP service/api.py
COPY configschema.json /home/tapis/configschema.json
COPY config-local.json /home/tapis/config.json
COPY service /home/tapis/service

RUN chown -R tapis:tapis /home/tapis
USER tapis
