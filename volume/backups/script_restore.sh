#!/bin/bash
DATE=$(date +"%Y-%m-%d")
SQL_FILE=/docker-entrypoint-initdb.d/db-${MYSQL_DATABASE}-${DATE}.sql
USER=${MYSQL_USER}
PASSWORD=${MYSQL_PASSWORD}
DATABASE=${MYSQL_DATABASE}

mariadb -u"${USER}" -p"${PASSWORD}" "${DATABASE}" < "${SQL_FILE}"
