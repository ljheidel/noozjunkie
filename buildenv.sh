#!/bin/bash
# Build the environment for noozjunkie
PATH="/usr/local/bin:/usr/bin:/sbin:/bin"

DIRS="tmp noozjunkie_webapp/static noozjunkie_webapp/templates"
MODS="flask flask-login flask-sqlalchemy sqlalchemy-migrate flask-restless requests praw feedparser flask-wtf flask-bcrypt flask_JWT"
DIR="flask"

for d in ${DIRS}; do
    if [  ! -e ${d} ]; then
        mkdir -p ${d}
    else
        echo ${d}' already exists.'
    fi
done

if [ ! -e ${DIR}/bin/python3 ]; then
    virtualenv ${DIR}
    if [ ${?} -ne 0 ]; then
        echo "Error creating virtual environment.  Exiting."
        exit 1
    fi
else
    echo 'Virtual environment appears to already exist in '${DIR}
fi
for m in ${MODS}; do
    ${DIR}/bin/pip3 install ${m}
    if [ ${?} -ne 0 ]; then
        echo "Error installing ${m}.  Exiting."
        exit 1
    fi
done

if [ ! -e newspaper ]; then
        git clone git://github.com/codelucas/newspaper.git
        if [ ${?} -ne 0 ]; then
            echo "Error cloning newspaper.  Exiting."
            exit 1
        fi 
        cd newspaper
        ../flask/bin/pip3 install -r requirements.txt
        if [ ${?} -ne 0 ]; then
            echo "Error installing dependencies for newspaper. Exiting."
            exit 1
        fi

        ../flask/bin/python3 ./setup.py install
        if [ ${?} -ne 0 ]; then
            echo "Error installing newspaper. Exiting."
            exit 1
        fi
        cd ..
fi

