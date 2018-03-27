
#https://stackoverflow.com/questions/592620/check-if-a-program-exists-from-a-bash-script

if [ -x "$(command -v gunicorn)" ]
then
    gunicorn --reload communication.server
else
    echo "gunicorn not installed"
    echo "sudo pip install gunicorn"
fi

