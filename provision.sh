#!/bin/bash

VIRTUALENV_DIR=/home/vagrant/.virtualenvs/riverhack
PROJECT_DIR=/vagrant/

PIP=$VIRTUALENV_DIR/bin/pip
PYTHON=$VIRTUALENV_DIR/bin/python

cat > /home/vagrant/.bashrc <<- EOM
source ~/.virtualenvs/riverhack/bin/activate
EOM

# Create virtualenv
su - vagrant -c "mkdir /home/vagrant/.virtualenvs/"
su - vagrant -c "/usr/local/bin/virtualenv $VIRTUALENV_DIR --python=/usr/bin/python3"
su - vagrant -c "echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"
su - vagrant -c "$PIP install -r $PROJECT_DIR/requirements.txt"

# create database
su - vagrant -c "createdb riverhack"

# migrate
su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py migrate"
