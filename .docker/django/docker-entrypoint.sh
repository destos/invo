#!/bin/sh
set -euo pipefail

# activate our virtual environment
. /opt/pysetup/.venv/bin/activate

# Initialize with empty value by default
DATABASE_URL=${DATABASE_URL:-""}

# Wait for Postgres for Django related commands.
if [[ $@ == *"manage.py "* && ! -z "$DATABASE_HOST" && -z "$DATABASE_URL" ]]
then
    RETRIES=60
    >&2 echo "Waiting for Postgres"
    until PGPASSWORD=$DATABASE_PASSWORD pg_isready -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USER ; do
        if [ $RETRIES -eq 0 ]; then
            >&2 echo "Exiting"
            exit
        fi
        >&2 echo "Waiting for Postgres server, $((RETRIES--)) remaining attempts"
        sleep 1
    done
fi

exec "$@"
