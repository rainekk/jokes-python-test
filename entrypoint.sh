#!/bin/sh
# move to folder
cd /opt/joke_api
# export variables
export FLASK_APP=joke_api
export FLASK_ENV=prodcution
# create database if not exists
if [ ! -f instance/joke_api.sqlite ]; then
  flask init-db
fi
# run application
flask run --host=0.0.0.0
