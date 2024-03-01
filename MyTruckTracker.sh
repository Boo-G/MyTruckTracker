#!/bin/bash

#change dir to project dir
cd ./team-28-cmpt-370

#install required extentions
pip install django
pip install django_hosts
pip install django-storage-url
pip install pillow
pip install pywebview
pip install psycopg2-binary

#open the server
python3 -m webbrowser http://127.0.0.1:8000/

#run the script
python3 manage.py runserver