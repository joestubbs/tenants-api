#!/bin/bash

cd /home/tapis/service; /usr/local/bin/gunicorn -w $threads -b :5000 api:app

while true; do sleep 86400; done