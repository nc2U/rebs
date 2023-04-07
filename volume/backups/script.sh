#!/bin/bash
DATE=$(date +"%Y-%m-%d")
SQL_FILE=/var/backups/db-${MYSQL_DATABASE}-${DATE}.sql
DATABASE=${MYSQL_DATABASE}
USER=${MYSQL_USER}
PASSWORD=${MYSQL_PASSWORD}

# (2) in case you run this more than once a day,
# remove the previous version of the file
# shellcheck disable=SC2046
rm -rf $(find ./ -name "*.sql"  -mtime +2 -delete)

# (3) do the mysql database backup (dump)
mysqldump -u"${USER}" -p"${PASSWORD}" "${DATABASE}" --ignore-table="${DATABASE}".django_migrations > "${SQL_FILE}"
