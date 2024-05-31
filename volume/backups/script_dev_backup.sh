#!/bin/bash
DATE=$(date +"%Y-%m-%d")
SQL_FILE=/var/backups/db-${MYSQL_DATABASE}-${DATE}.sql
USER=${MYSQL_USER}
PASSWORD=${MYSQL_PASSWORD}
DATABASE=${MYSQL_DATABASE}

mariadb -u"${USER}" -p"${PASSWORD}" "${DATABASE}" < /docker-entrypoint-initdb.d/"${SQL_FILE}"
