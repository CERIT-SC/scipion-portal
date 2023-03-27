#!/bin/bash
set -xe

cd /srv/scipo
python3 manage.py collectstatic

# init required data in the database
python3 manage.py migrate sessions
python3 manage.py migrate auth

#python3 manage.py runserver_plus --cert-file /mnt/cert/fullchain.pem --key-file /mnt/cert/privkey.pem 0.0.0.0:443
python3 manage.py runserver 0.0.0.0:8080
