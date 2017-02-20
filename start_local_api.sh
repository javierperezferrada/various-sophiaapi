#!/bin/bash
#start all environment to Develope SophiaAPI
gnome-terminal --tab -e "python SophiaAPI/SophiaAPI/manage.py runserver 8000" --tab -e "./elasticsearch-2.2.0/bin/elasticsearch"
gnome-terminal --tab -e "sudo service mongod start"

