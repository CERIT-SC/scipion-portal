#!/bin/bash

cd /srv/scipo
python3 manage.py collectstatic

#python3 manage.py runserver_plus --cert-file /mnt/cert/fullchain.pem --key-file /mnt/cert/privkey.pem 0.0.0.0:443
python3 manage.py runserver 0.0.0.0:80
