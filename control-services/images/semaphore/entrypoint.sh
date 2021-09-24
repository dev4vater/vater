#!/bin/sh
test_db_connect() {
    echo "Test connect to ${SEMAPHORE_DB_HOST} with user:pass ${SEMAPHORE_DB_USER}:${SEMAPHORE_DB_PASS}"
    until mysql -h ${SEMAPHORE_DB_HOST} -u ${SEMAPHORE_DB_USER} --password=${SEMAPHORE_DB_PASS} ${SEMAPHORE_DB} -e "select version();" &>/dev/null;
    do
        echo "Waiting database connection..."
        sleep 3
    done
}

init_semaphore_config() {
    if [ -f /data/semaphore_config.json ]
    then
        echo "already initialized"
    else
        echo "Initializing semaphore"
        ( cat <<EOF
${SEMAPHORE_DB_HOST}:${SEMAPHORE_DB_PORT}
${SEMAPHORE_DB_USER}
${SEMAPHORE_DB_PASS}
${SEMAPHORE_DB}
${SEMAPHORE_PLAYBOOK_PATH}
yes
${SEMAPHORE_ADMIN}
${SEMAPHORE_ADMIN_EMAIL}
${SEMAPHORE_ADMIN_NAME}
${SEMAPHORE_ADMIN_PASSWORD}
EOF
) | /usr/bin/semaphore -setup
    fi
}

if [ -f /data/semaphore_config.sh ]
then
    . /data/semaphore_config.sh
    test_db_connect
    init_semaphore_config
fi

# run our command
exec "$@"
