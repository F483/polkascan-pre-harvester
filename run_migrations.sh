#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./run_migrations.sh <development|test>"
    exit 1
fi

if [ $1 != "development" ] && [ $1 != "test" ]; then
    echo "Usage: ./run_migrations.sh <development|test>"
    exit 1
fi

if [ $1 == "development" ]; then
    export DB_CONNECTION="mysql+mysqlconnector://$DB_USERNAME:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME"
fi

if [ $1 == "test" ]; then
    export DB_CONNECTION="mysql+mysqlconnector://$DB_USERNAME_TEST:$DB_PASSWORD_TEST@$DB_HOST_TEST:$DB_PORT_TEST/$DB_NAME_TEST"
fi

alembic upgrade head
