#!/usr/bin/env bash

usage() {
  echo "Usage: ./manage_influx_database.sh DATABASE_NAME"
}

influxcmd() {
  local cmd="$1"

  echo "Execute command \"${cmd}\""
  influx -execute "${cmd}"

}

if [ $# -ne 1 ]
then
  usage
  exit 1
fi

DATABASE_NAME="$1"
CHANGED=0

RESULT=$(influx -execute 'SHOW DATABASES' | grep "^${DATABASE_NAME}")
if [ $? -ne 0 ]
then
  influxcmd "CREATE DATABASE ${DATABASE_NAME}"
  exit 10
fi

exit 0
