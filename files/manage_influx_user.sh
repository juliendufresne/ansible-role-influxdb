#!/usr/bin/env bash
set -e

USER_TYPE=
USER_NAME=
USER_PASSWORD=

usage() {
  echo "Usage: ./manage_influx_users.sh --user-type admin|user --user-name USER_NAME --user-password USER_PASSWORD [LIST_OF_RIGHTS]"
  echo "      LIST_OF_RIGHTS:  DB_NAME:(ALL|READ|WRITE)"
}

while [[ $# -ge 1 ]]
do
    case "$1" in
        --user-type)
            USER_TYPE="$2"
            shift
            shift
            if [ "${USER_TYPE}" != "user" ] && [ "${USER_TYPE}" != "admin" ]
            then
                echo "Wrong user type"
                usage
                exit 1
            fi
        ;;
        --user-name) USER_NAME="$2"; shift; shift ;;
        --user-password) USER_PASSWORD="$2"; shift; shift ;;
        *) break ;;
    esac
done

if [ -z "${USER_TYPE}" ]
then
    echo "--user-type option is mandatory"
    usage
    exit 1
fi

if [ -z "${USER_NAME}" ]
then
    echo "--user-name option is mandatory"
    usage
    exit 1
fi

if [ -z "${USER_PASSWORD}" ]
then
    echo "--user-password option is mandatory"
    usage
    exit 1
fi

CHANGED=0
if ! influx -execute 'SHOW USERS' | grep -q "^${USER_NAME}"
then
    influx -execute "CREATE USER ${USER_NAME} WITH PASSWORD '${USER_PASSWORD}'"
    CHANGED=1
fi

RESULT=$(influx -execute 'SHOW USERS' | grep "^${USER_NAME}")
if [ "$USER_TYPE" == "admin" ]
then
    if ! echo ${RESULT} | grep "true"
    then
        influx -execute "GRANT ALL PRIVILEGES TO ${USER_NAME}"
        CHANGED=1
    fi
elif [ "$USER_TYPE" == "user" ]
then
    if ! echo ${RESULT} | grep -q "false"
    then
        influx -execute "REVOKE ALL PRIVILEGES FROM ${USER_NAME}"
        CHANGED=1
    fi
fi
# Since we can not know if a user's password has changed, we reset it and do not trigger the CHANGED variable
influx -execute "SET PASSWORD FOR ${USER_NAME} = '${USER_PASSWORD}'"

# Manage database rights
while [[ $# -ge 1 ]]
do
    IFS=':' read -ra RIGHTS <<< "$1"
    DBNAME=${RIGHTS[0]}
    CURRENT_RIGHT=""
    if influx -execute "SHOW GRANTS FOR ${USER_NAME}" | grep -q "^${DBNAME}"
    then
        CURRENT_RIGHT=$(influx -execute "SHOW GRANTS FOR ${USER_NAME}" | grep "^${DBNAME}")
    fi

    case "${RIGHTS[1]}" in
        "ALL")
            if ! echo "${CURRENT_RIGHT}" | grep -q "ALL PRIVILEGES"
            then
                influx -execute "GRANT ALL ON ${DBNAME} TO ${USER_NAME}"
                CHANGED=1
            fi
        ;;
        "READ")
            if ! echo "${CURRENT_RIGHT}" | grep -q "READ"
            then
                influx -execute "REVOKE WRITE ON ${DBNAME} FROM ${USER_NAME}"
                influx -execute "GRANT READ ON ${DBNAME} TO ${USER_NAME}"
                CHANGED=1
            fi
        ;;
        "WRITE")
            if ! echo "${CURRENT_RIGHT}" | grep -q "WRITE"
            then
                influx -execute "REVOKE READ ON ${DBNAME} FROM ${USER_NAME}"
                influx -execute "GRANT WRITE ON ${DBNAME} TO ${USER_NAME}"
                CHANGED=1
            fi
        ;;
        *)
            echo "malformed DB_NAME:RIGHT expects RIGHT to be one of ALL, READ or WRITE"
            usage
            exit 1
        ;;
    esac
    shift
done

if [ ${CHANGED} -eq 1 ]
then
    exit 10
fi
exit 0
