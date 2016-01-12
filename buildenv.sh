#!/bin/bash
# Build the environment for noozjunkie

DIRS="tmp noozjunkie_webapp/static noozjunkie_webapp/templates"
MODS="flask flask-login flask-sqlalchemy sqlalchemy-migrate flask-restless newspaper praw feedparser flask-wtf flask-bcrypt"
DIR="flask"

for d in ${DIRS}; do
    if [  ! -e ${d} ]; then
        mkdir -p ${d}
    else
        echo ${d}' already exists.'
    fi
done
pip3 install virtualenv
if [ ! -e ${DIR}/bin/python3 ]; then
    virtualenv flask
else
    echo 'Virtual environment appears to exist in '${DIR}
fi
for m in ${MODS}; do
    ${DIR}/bin/pip3 install ${m}
done
