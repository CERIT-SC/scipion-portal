#!/bin/bash

cd /srv/scipo
python3 manage.py migrate

python3 manage.py runserver 0.0.0.0:8080
