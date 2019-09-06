# image: tapis/flaskbase
# Base image for building Tapis API services in Python/flask
from python:3.7

RUN useradd tapis
ADD requirements.txt /home/tapis/common-requirements.txt

RUN pip install -U --no-cache-dir pip && \
    pip install --no-cache-dir -r /home/tapis/common-requirements.txt

# ----Add the common lib (eventually this could be a pip install)
COPY common /usr/local/lib/python3.7/site-packages/common

# TODO -- eventually remove this
RUN apt-get update && apt-get install -y vim

# set default threads for gunicorn
ENV threads=3

WORKDIR /home/tapis

COPY service_entry.sh /home/tapis/entry.sh
RUN chmod +x /home/tapis/entry.sh

CMD ["./entry.sh"]


