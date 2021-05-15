#!/bin/bash
docker run --rm -it -p 80:5000 -v $PWD/flask-project:/data biodepot/flask:test python3 /data/app.py
