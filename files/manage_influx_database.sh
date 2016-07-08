#!/usr/bin/env bash

usage() {
    echo "Usage: ./manage_influx_database.sh DATABASE_NAME"
}

if [ $# -ne 1 ]
then
    usage
    exit 1
fi

DATABASE_NAME="$1"
CHANGED=0

if influx -execute 'SHOW DATABASES' | grep -q "^${DATABASE_NAME}"
then
    exit 0
fi

if ! influx -execute "CREATE DATABASE ${DATABASE_NAME}"
then
    exit 1
fi
exit 10
