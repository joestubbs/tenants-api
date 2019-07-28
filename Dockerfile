# image: tapis/tenants-api
from python:3.7

RUN useradd tapis
ADD requirements.txt /home/tapis/requirements.txt

RUN pip install -U --no-cache-dir pip && \
    pip install --no-cache-dir -r /home/tapis/requirements.txt

RUN chown -R tapis:tapis /home/tapis
WORKDIR /home/tapis
USER tapis

# ----API specific code
ENV TAPIS_API tenants
COPY tenants /home/tapis/service