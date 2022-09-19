#!/bin/bash

while ! nc -z $MYSQL_DB_HOST $MYSQL_DB_PORT; do
  echo "WAITING FOR CONNECTION..."
  sleep 5
done

echo "MySQL started..."

python manage.py db_migration

exec "$@"