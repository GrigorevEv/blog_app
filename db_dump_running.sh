#!/bin/bash

docker exec -it blog_app_web_1 python manage.py dumpdata > blog_dump.json
