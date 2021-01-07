#!/bin/sh
set -e

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
#PYTHON="$SCRIPTPATH/../venv/bin/python"
#PIP="$SCRIPTPATH/../venv/bin/pip"

echo "Deploying application ..."

#cd $(dirname $SCRIPTPATH)

# Update codebase
git fetch origin production
git reset --hard origin/production

$PIP install -r requirements.txt

# collect static stuff
$PYTHON manage.py collectstatic --noinput;

# Migrate database
$PYTHON manage.py migrate

systemctl --user restart django_deploy_test

echo "Application deployed!"
