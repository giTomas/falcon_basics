#!/usr/bin/env bash

#https://stackoverflow.com/questions/592620/check-if-a-program-exists-from-a-bash-script

if [ -x "$(command -v gunicorn)" ]; then
    LOOK_STORAGE_PATH=/tmp gunicorn --reload 'look.app:get_app()'
else
    echo "Gunicorn server not installed"
    echo "sudo pip install gunicorn"
fi

