#!/usr/bin/env sh

python ./manage.py migrate
gunicorn --forwarded-allow-ips=* --bind 0.0.0.0:8080 -w 2 mshp_ctf.wsgi:application