#!/usr/bin/env bash

CONTAINER_ID=backend

_usage() {
    echo "--- Backend PostgreSQL Usage ---"
    echo "usage: $0 help                        # Display this usage message"
    echo "usage: $0 start                       # Starts backend database container"
    echo "usage: $0 stop                        # Stops backend database container"
    echo "usage: $0 restart                     # restarts backend database container"
    echo "usage: $0 dbshell                     # Connects to backend database as postgres user"
    echo "usage: $0 dbshell USER PASS DATABASE  # Connects to backend DATABASE as USERNAME"
    echo "usage: $0 purge                       # Remove backend database and all contents"
}

_start() {
    if [[ "$(docker ps -a | grep backend)" ]]; then
        if [[ $(docker inspect -f {{.State.Running}} ${CONTAINER_ID}) != 'true' ]]; then
            docker-compose start ${CONTAINER_ID}
        else
            echo "${CONTAINER_ID} is already running..."
        fi
    else
        docker-compose up -d
    fi
}

_stop() {
    if [[ $(docker inspect -f {{.State.Running}} ${CONTAINER_ID}) = 'true' ]]; then
        docker-compose stop ${CONTAINER_ID}
    else
        echo "${CONTAINER_ID} is not running..."
    fi
}

_restart() {
    _stop
    _start
}

_dbshell() {
    if [[ $# -eq 1 ]]; then
        # connect to database as postgres user
        docker exec -ti -u postgres ${CONTAINER_ID} psql
    elif [[ $# -eq 4 ]]; then
        # hostname:port:database:username:password
        docker exec ${CONTAINER_ID} /usr/bin/env bash -c 'install -m 0600 /dev/null /root/.pgpass'
        docker exec ${CONTAINER_ID} /usr/bin/env bash -c 'echo "localhost:5432:'${4}':'${2}':'${3}'" >> /root/.pgpass'
        docker exec -ti ${CONTAINER_ID} psql -h localhost -U ${2} ${4}
    else
        echo "Invalid request..."
        echo "usage: $0 prompt                      # Connects to backend database as postgres user"
        echo "usage: $0 prompt USER PASS DATABASE   # Connects to backend DATABASE as USERNAME"
    fi
}

_purge() {
    _stop
    docker-compose rm -f ${CONTAINER_ID}
}

case "$1" in
    help) _usage
        ;;
    start) _start
        ;;
    stop) _stop
        ;;
    restart) _restart
        ;;
    dbshell) _dbshell "$@"
        ;;
    purge) _purge
        ;;
    *) _usage
        ;;
esac

exit 0;
